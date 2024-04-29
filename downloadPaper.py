import sys
import requests
from handlers import StatusHandler

def downloadPaper(id):
    status = StatusHandler(id)
    
    if status.isPaperDownloaded():
        raise ValueError("Paper already downloaded")
    
    pdfURL = "https://www.dovepress.com/getfile.php?fileID=15943"
    
    res = requests.get(pdfURL)
    if res.status_code != 200:
        print(res.reason)
        raise requests.exceptions.RequestException("Failed to fetch PDF")
    
    # END TODO
        
    statusData = status.get()
    statusData["downloadPaper"] = {
        "status": "downloaded",
        "filename": f"{id}.pdf"
    }
    
    status.update(statusData)
    print(status.get())
    
    with open(status.getPDFPath(), "wb") as pdfFile:
        pdfFile.write(res.content)
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python download_paper.py <paper_id>")
        sys.exit(1)
        
    id = sys.argv[1]
    
    try:
        downloadPaper(id)
    except Exception as err:
        print(f"Error downloading paper: {err}")