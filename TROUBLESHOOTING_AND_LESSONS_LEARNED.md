# BikeStore Power BI Analytics: Troubleshooting & Lessons Learned

> **Tài liệu tổng hợp các lỗi phát sinh trong quá trình triển khai dự án Power BI (PBIP/PBIR), nguyên nhân gốc rễ, giải pháp khắc phục và bài học kinh nghiệm.**

---

## Mục lục
1. [Lỗi 1: Power Query - Không tìm thấy bảng Excel (`KeyNotFoundException`)](#lỗi-1-power-query---không-tìm-thấy-bảng-excel-keynotfoundexception)
2. [Lỗi 2: Dữ liệu Excel có dòng trống gây lỗi chuyển đổi kiểu & hỏng Relationship (`DataFormat.Error`)](#lỗi-2-dữ-liệu-excel-có-dòng-trống-gây-lỗi-chuyển-đổi-kiểu--hỏng-relationship-dataformaterror)
3. [Lỗi 3: Đường dẫn file nguồn bị cố định (Hardcoded File Path)](#lỗi-3-đường-dẫn-file-nguồn-bị-cố-định-hardcoded-file-path)
4. [Lỗi 4: Lệch tên Schema/Column/Measure làm hỏng Visuals ("Can't display this visual")](#lỗi-4-lệch-tên-schemacolumnmeasure-làm-hỏng-visuals-cant-display-this-visual)
5. [Lỗi 5: Cấu trúc JSON Visual trong PBIP v1.0 (`config` Stringified JSON)](#lỗi-5-cấu-trúc-json-visual-trong-pbip-v10-config-stringified-json)
6. [Lỗi 6: Mã hóa file UTF-8 BOM gây lỗi parser trên Windows PowerShell](#lỗi-6-mã-hóa-file-utf-8-bom-gây-lỗi-parser-trên-windows-powershell)
7. [Lỗi 7: Môi trường Windows thiếu Python / Microsoft Store Execution Alias](#lỗi-7-môi-trường-windows-thiếu-python--microsoft-store-execution-alias)
8. [Lỗi 8: Không đồng bộ giữa TMDL và `model.bim`](#lỗi-8-không-đồng-bộ-giữa-tmdl-và-modelbim)
9. [Bảng tổng hợp Checklist kiểm tra chất lượng (QA Checklist)](#bảng-tổng-hợp-checklist-kiểm-tra-chất-lượng-qa-checklist)

---

## Lỗi 1: Power Query - Không tìm thấy bảng Excel (`KeyNotFoundException`)

### Hiện tượng
Khi Power BI Desktop thực hiện Data Refresh, các bảng như `Dim_Product`, `Fact_Sales`, `Dim_Staff` báo lỗi:
> `The key didn't match any rows in the table` hoặc `KeyNotFoundException`.

### Nguyên nhân gốc rễ
Trong code M ban đầu sử dụng:
```powerquery
products_Table = Source{[Item="products", Kind="Table"]}[Data]
```
File `BikeStore.xlsx` được lưu dưới dạng các **Worksheet thông thường**, không phải bảng có cấu trúc Excel Table chính thức (`ListObject`). Do đó, bộ lọc `Kind="Table"` không tìm thấy bất kỳ dòng nào khớp.

### Giải pháp khắc phục
Đổi toàn bộ sang `Kind="Sheet"` và bổ sung bước `Table.PromoteHeaders`:
```powerquery
products_Sheet = Source{[Item="products", Kind="Sheet"]}[Data],
#"Promoted Products" = Table.PromoteHeaders(products_Sheet, [PromoteAllScalars=true])
```

---

## Lỗi 2: Dữ liệu Excel có dòng trống gây lỗi chuyển đổi kiểu & hỏng Relationship (`DataFormat.Error`)

### Hiện tượng
1. Chuyển đổi kiểu dữ liệu sang số (`Int64.Type`) báo lỗi: `DataFormat.Error: We couldn't convert to Number` tại các dòng có giá trị chuỗi rỗng `""`.
2. Khi thiết lập mối quan hệ `1:*` giữa `Dim_Customer` hoặc `Dim_Store` với `Fact_Sales`, Power BI báo lỗi Cardinality do cột khóa chính chứa nhiều giá trị `null` / rỗng.

### Nguyên nhân gốc rễ
File Excel thường có các dòng định dạng trống kéo dài phía cuối sheet. Khi nạp vào Power Query, các dòng này trở thành các dòng dữ liệu trống với giá trị `""` hoặc `null`.

### Giải pháp khắc phục
Ngay sau bước `Table.PromoteHeaders`, luôn luôn thêm bước lọc bỏ triệt để các dòng trống trên cột khóa chính:
```powerquery
#"Filtered Blank Rows" = Table.SelectRows(#"Promoted Headers", each [customer_id] <> null and [customer_id] <> "")
```

---

## Lỗi 3: Đường dẫn file nguồn bị cố định (Hardcoded File Path)

### Hiện tượng
Khi mở file `.pbip` trên máy khác hoặc di chuyển thư mục dự án, Power Query không thể refresh được dữ liệu do đường dẫn file Excel `BikeStore.xlsx` bị hardcode tuyệt đối (`C:\Data\...`).

### Giải pháp khắc phục
1. Khai báo Power Query Parameter `FilePath`:
```powerquery
FilePath = "C:\Users\minle\.gemini\antigravity-ide\scratch\bikestore-powerbi-analytics\BikeStore.xlsx" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```
2. Mọi bảng dữ liệu đều trỏ vào `FilePath`:
```powerquery
Source = Excel.Workbook(File.Contents(FilePath), null, true)
```
3. Người dùng khi chuyển máy chỉ cần vào `Home > Transform Data > Edit Parameters` để sửa đường dẫn 1 lần duy nhất cho toàn bộ báo cáo.

---

## Lỗi 4: Lệch tên Schema/Column/Measure làm hỏng Visuals ("Can't display this visual")

### Hiện tượng
Khi mở file `report.json`, một loạt visual hiển thị dấu chấm than đỏ:
> `"Can't display this visual"`
> `"The column 'Brand Name' does not exist in table 'Dim_Product'"`
> `"Table '_Measures' does not contain measure 'Completed Orders Count'"`

### Nguyên nhân gốc rễ
1. Script tạo visual tự động đặt tên theo cảm tính hoặc có khoảng trắng:
   - Dùng `Brand Name` thay vì tên thực tế `Brand_Name`.
   - Dùng `Category Name` thay vì `Category_Name`.
   - Dùng `Customer Full Name` thay vì `Customer_Name`.
   - Dùng `Order Status Description` thay vì `Order_Status`.
2. Visual liên kết đến các measure không tồn tại trong model (ví dụ: `Completed Orders Count`, `Avg Days to Ship`, `Current Inventory Units`, `Inventory Valuation`).

### Giải pháp khắc phục
- Rà soát toàn bộ Semantic Model (`_Measures.tmdl` và `model.bim`) để lấy danh sách cột và measure chuẩn 100%.
- Cập nhật script tự động sinh visual (`generate_report_visuals.ps1` & `generate_report_visuals.py`) khớp từng ký tự:
  - Cột: `Brand_Name`, `Category_Name`, `Store_Name`, `Staff_Name`, `Customer_Name`, `Order_Status`, `YearMonth`.
  - Measures: `Total Net Revenue`, `Total Orders`, `Average Order Value`, `Total Units Sold`, `Total Active Customers`, `Total Stock Quantity`, `Total Stock Value`, `Total Gross Revenue`, `Average Discount %`, `Revenue Per Customer`.

---

## Lỗi 5: Cấu trúc JSON Visual trong PBIP v1.0 (`config` Stringified JSON)

### Hiện tượng
File `report.json` bị lỗi parse hoặc Power BI Desktop bỏ qua toàn bộ danh sách `visualContainers`.

### Nguyên nhân gốc rễ
Trong định dạng Power BI Project v1.0 (`report.json`), thuộc tính `"config"` bên trong mỗi phần tử `visualContainers` **không phải là JSON object lồng nhau**, mà bắt buộc phải là **chuỗi JSON đã escape (Stringified JSON)**:
```json
// SAI:
"config": { "name": "abc", "singleVisual": { ... } }

// ĐÚNG:
"config": "{\"name\":\"abc\",\"layouts\":[...],\"singleVisual\":{...}}"
```

### Giải pháp khắc phục
- Trong PowerShell: Dùng `$configObj | ConvertTo-Json -Depth 10 -Compress`
- Trong Python: Dùng `json.dumps(config_obj, ensure_ascii=False)`

---

## Lỗi 6: Mã hóa file UTF-8 BOM gây lỗi parser trên Windows PowerShell

### Hiện tượng
File `report.json` sau khi ghi bằng PowerShell bị lỗi parsing khi mở trong Power BI Desktop hoặc tạo ra ký tự lạ `\ufeff` trong Git diff.

### Nguyên nhân gốc rễ
Lệnh `Set-Content` hoặc `Out-File` mặc định của Windows PowerShell 5.1 lưu file ở định dạng UTF-16 LE hoặc UTF-8 có Byte Order Mark (BOM).

### Giải pháp khắc phục
Sử dụng trực tiếp lớp .NET `System.Text.UTF8Encoding($false)` để đảm bảo ghi file chuẩn UTF-8 No BOM:
```powershell
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText((Resolve-Path $reportPath).Path, $finalJson, $utf8NoBom)
```

---

## Lỗi 7: Môi trường Windows thiếu Python / Microsoft Store Execution Alias

### Hiện tượng
Khi chạy `python generate_report_visuals.py`, hệ thống trả về:
> `Python was not found; run without arguments to install from the Microsoft Store...`

### Nguyên nhân gốc rễ
Nhiều máy tính Windows của người dùng Power BI không cài sẵn Python trong biến môi trường PATH hoặc bị App Execution Alias của Windows chặn.

### Giải pháp khắc phục
Xây dựng script **`generate_report_visuals.ps1` bằng 100% PowerShell nguyên bản**, không phụ thuộc bất kỳ thư viện bên ngoài nào, sẵn sàng chạy ngay trên mọi máy tính Windows:
```powershell
powershell -ExecutionPolicy Bypass -File .\generate_report_visuals.ps1
```

---

## Lỗi 8: Không đồng bộ giữa TMDL và `model.bim`

### Hiện tượng
Khi chỉnh sửa các truy vấn M trong thư mục `definition/tables/*.tmdl`, mở lại qua file `.pbip` thì một số công cụ hoặc phiên bản Power BI cũ vẫn đọc file `model.bim` cũ chưa có bước lọc dòng trống.

### Giải pháp khắc phục
Đồng bộ song song cả 2 định dạng:
1. Thư mục TMDL `BikeStore_Analytics.SemanticModel/definition/` (chuẩn PBIP mới).
2. File `BikeStore_Analytics.SemanticModel/model.bim` (chuẩn Tabular Object Model).
Đảm bảo cả 2 đều chứa cùng một định nghĩa M, cùng danh sách Measure và cùng cấu trúc quan hệ.

---

## Bảng tổng hợp Checklist kiểm tra chất lượng (QA Checklist)

| STT | Hạng mục kiểm tra | Tiêu chí đạt | Đã kiểm tra |
| :--- | :--- | :--- | :---: |
| 1 | **Excel Loading** | Sử dụng `Kind="Sheet"` kèm `PromoteAllScalars=true` | ✅ |
| 2 | **Blank Rows** | Có bước `Table.SelectRows` lọc dòng trống trên khóa chính | ✅ |
| 3 | **Parameterization** | FilePath là tham số `meta [IsParameterQuery=true]` | ✅ |
| 4 | **Star Schema** | Quan hệ 1:* đơn hướng từ Dim sang Fact, không có Bi-directional | ✅ |
| 5 | **Visual Naming** | 100% tên cột và measure khớp chính xác với `model.bim` | ✅ |
| 6 | **report.json Config** | Trường `config` là stringified JSON nén | ✅ |
| 7 | **File Encoding** | Lưu trữ chuẩn UTF-8 Không có BOM | ✅ |
| 8 | **Portability** | Có sẵn script PowerShell `.ps1` chạy ngay trên Windows | ✅ |
| 9 | **GitHub Sync** | Toàn bộ mã nguồn, cấu hình và skills được push lên git remote | ✅ |
