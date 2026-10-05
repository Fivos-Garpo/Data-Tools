from pathlib import Path
import json
import pandas as pd

COLUMNS = ["__time","timestamp","meter_address","snr","rssi","spFact","telegram","gateway_id"]

def _load(path):
    ext = Path(path).suffix.lower()
    if ext in {".json", ".txt"}:
        with open(path, "r", encoding="utf-8") as f:
            return pd.DataFrame(json.load(f).get("events", []))
    if ext == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"Unsupported file type: {ext}")

def generate_infra_report(input_files, excel_name="snr_sf_summary", time_bin="w", per_device=True):
    frames = []
    for file in input_files:
        try:
            df = _load(file)
            for col in COLUMNS:
                if col not in df.columns:
                    df[col] = None
            frames.append(df[COLUMNS])
        except Exception:
            continue
    if not frames:
        raise ValueError("No valid data found.")
    data = pd.concat(frames, ignore_index=True)
    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce").dt.tz_localize(None)
    data = data.dropna(subset=["timestamp", "meter_address"]).copy()
    for col in ["snr","rssi","spFact"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    data["Noise_Floor"] = data["rssi"] - data["snr"]
    data = data.sort_values("timestamp").reset_index(drop=True)
    data.insert(0, "ID", range(1, len(data) + 1))
    freq = {"d":"D", "w":"7D", "m":"ME"}.get(time_bin.lower(), "7D")
    data["time_bin"] = (data["timestamp"].dt.to_period("M").dt.to_timestamp()
                        if freq == "ME" else data["timestamp"].dt.floor(freq))
    output = Path(input_files[0]).parent / f"{excel_name}.xlsx"
    with pd.ExcelWriter(output, engine="xlsxwriter", datetime_format="dd/mm/yyyy hh:mm:ss") as writer:
        raw = data[["__time","timestamp","meter_address","snr","rssi","spFact","telegram","gateway_id","Noise_Floor"]]
        raw.to_excel(writer, index=False, sheet_name="RawData")
        sf = data.groupby(["time_bin","spFact"])["meter_address"].nunique().unstack(fill_value=0)
        sf.to_excel(writer, sheet_name="SF_Count")
        snr = data.groupby("time_bin")["snr"].mean().rename("Average_SNR").reset_index()
        snr.to_excel(writer, index=False, sheet_name="SNR_Avg_Over_Time")
        noise = data.groupby("time_bin")["Noise_Floor"].mean().rename("Average_Noise_Floor").reset_index()
        noise.to_excel(writer, index=False, sheet_name="Noise_Avg_Over_Time")
        wb = writer.book
        for sheet, title, value_col in [
            ("SNR_Avg_Over_Time","Average SNR",1),
            ("Noise_Avg_Over_Time","Average Noise Floor",1)
        ]:
            ws = writer.sheets[sheet]
            end = len(data.groupby("time_bin"))
            chart = wb.add_chart({"type":"line"})
            chart.add_series({"name":title,"categories":[sheet,1,0,end,0],"values":[sheet,1,value_col,end,value_col]})
            chart.set_title({"name":title})
            ws.insert_chart("D2", chart)
        if per_device:
            for device, subset in data.groupby("meter_address"):
                name = str(device).replace(":","_").replace("/","_")[:31] or "Device"
                if name in writer.sheets:
                    continue
                subset[["timestamp","snr","rssi","spFact","telegram","gateway_id","Noise_Floor"]].to_excel(
                    writer, index=False, sheet_name=name)
    return output
