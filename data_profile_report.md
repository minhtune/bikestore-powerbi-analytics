# Power BI Data Profile Report: `BikeStore.xlsx`

## 1. Executive Summary

- **Total Tables / Sheets**: 9
- **Total Records Across Tables**: 9,071

### Table Catalog

| Table Name | Row Count | Column Count | Primary Key Candidate | Suggested Role |
| :--- | :--- | :--- | :--- | :--- |
| **stores** | 3 | 8 | `store_id, store_name, phone, email, street, city, state, zip_code` | **Dimension Table** |
| **stocks** | 939 | 3 | `None (Composite/Transaction)` | **Fact Table** |
| **staffs** | 10 | 8 | `staff_id, first_name, last_name, email, phone` | **Dimension Table** |
| **products** | 321 | 6 | `product_id` | **Dimension Table** |
| **orders** | 1,615 | 8 | `order_id` | **Fact Table** |
| **order_items** | 4,722 | 6 | `None (Composite/Transaction)` | **Fact Table** |
| **customers** | 1,445 | 9 | `customer_id, email, street` | **Dimension Table** |
| **categories** | 7 | 2 | `category_id, category_name` | **Dimension Table** |
| **brands** | 9 | 2 | `brand_id, brand_name` | **Dimension Table** |


## 2. Detected Relationships (Star Schema Map)

| Fact / Child Table | Foreign Key | Dimension / Parent Table | Primary Key | Relationship Cardinality |
| :--- | :--- | :--- | :--- | :--- |
| `stores` | `phone` | `staffs` | `phone` | **One-to-One (1:1)** |
| `stores` | `email` | `staffs` | `email` | **One-to-One (1:1)** |
| `stores` | `email` | `customers` | `email` | **One-to-One (1:1)** |
| `stores` | `street` | `customers` | `street` | **One-to-One (1:1)** |
| `stocks` | `store_id` | `stores` | `store_id` | **Many-to-One (*:1)** |
| `stocks` | `product_id` | `products` | `product_id` | **Many-to-One (*:1)** |
| `staffs` | `email` | `stores` | `email` | **One-to-One (1:1)** |
| `staffs` | `email` | `customers` | `email` | **One-to-One (1:1)** |
| `staffs` | `phone` | `stores` | `phone` | **One-to-One (1:1)** |
| `staffs` | `store_id` | `stores` | `store_id` | **Many-to-One (*:1)** |
| `products` | `brand_id` | `brands` | `brand_id` | **Many-to-One (*:1)** |
| `products` | `category_id` | `categories` | `category_id` | **Many-to-One (*:1)** |
| `orders` | `customer_id` | `customers` | `customer_id` | **Many-to-One (*:1)** |
| `orders` | `store_id` | `stores` | `store_id` | **Many-to-One (*:1)** |
| `orders` | `staff_id` | `staffs` | `staff_id` | **Many-to-One (*:1)** |
| `order_items` | `order_id` | `orders` | `order_id` | **Many-to-One (*:1)** |
| `order_items` | `product_id` | `products` | `product_id` | **Many-to-One (*:1)** |
| `customers` | `first_name` | `staffs` | `first_name` | **Many-to-One (*:1)** |
| `customers` | `last_name` | `staffs` | `last_name` | **Many-to-One (*:1)** |
| `customers` | `phone` | `stores` | `phone` | **Many-to-One (*:1)** |
| `customers` | `phone` | `staffs` | `phone` | **Many-to-One (*:1)** |
| `customers` | `email` | `stores` | `email` | **One-to-One (1:1)** |
| `customers` | `email` | `staffs` | `email` | **One-to-One (1:1)** |
| `customers` | `street` | `stores` | `street` | **One-to-One (1:1)** |
| `customers` | `city` | `stores` | `city` | **Many-to-One (*:1)** |
| `customers` | `state` | `stores` | `state` | **Many-to-One (*:1)** |
| `customers` | `zip_code` | `stores` | `zip_code` | **Many-to-One (*:1)** |


## 3. Table Column Profiles & Quality Checks

### Table: `stores` (3 rows, 8 columns)

| Column | Data Type | Nulls (%) | Distinct Count | Sample Values | Range / Min-Max |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `store_id` 🔑 *(PK)* | `int64` | 0.0% (0) | 3 | 1, 2, 3 | [1.0 to 3.0] |
| `store_name` 🔑 *(PK)* | `str` | 0.0% (0) | 3 | Santa Cruz Bikes, Baldwin Bikes, Rowlett Bikes | - |
| `phone` 🔑 *(PK)* | `str` | 0.0% (0) | 3 | (831) 476-4321, (516) 379-8888, (972) 530-5555 | - |
| `email` 🔑 *(PK)* | `str` | 0.0% (0) | 3 | santacruz@bikes.shop, baldwin@bikes.shop, rowlett@bikes.shop | - |
| `street` 🔑 *(PK)* | `str` | 0.0% (0) | 3 | 3700 Portola Drive, 4200 Chestnut Lane, 8000 Fairway Avenue | - |
| `city` 🔑 *(PK)* | `str` | 0.0% (0) | 3 | Santa Cruz, Baldwin, Rowlett | - |
| `state` 🔑 *(PK)* | `str` | 0.0% (0) | 3 | CA, NY, TX | - |
| `zip_code` 🔑 *(PK)* | `int64` | 0.0% (0) | 3 | 95060, 11432, 75088 | [11432.0 to 95060.0] |


### Table: `stocks` (939 rows, 3 columns)

| Column | Data Type | Nulls (%) | Distinct Count | Sample Values | Range / Min-Max |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `store_id` | `int64` | 0.0% (0) | 3 | 1, 2, 3 | [1.0 to 3.0] |
| `product_id` | `int64` | 0.0% (0) | 313 | 1, 2, 3 | [1.0 to 313.0] |
| `quantity` | `int64` | 0.0% (0) | 31 | 27, 5, 6 | [0.0 to 30.0] |


### Table: `staffs` (10 rows, 8 columns)

| Column | Data Type | Nulls (%) | Distinct Count | Sample Values | Range / Min-Max |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `staff_id` 🔑 *(PK)* | `int64` | 0.0% (0) | 10 | 1, 2, 3 | [1.0 to 10.0] |
| `first_name` 🔑 *(PK)* | `str` | 0.0% (0) | 10 | Fabiola, Mireya, Genna | - |
| `last_name` 🔑 *(PK)* | `str` | 0.0% (0) | 10 | Jackson, Copeland, Serrano | - |
| `email` 🔑 *(PK)* | `str` | 0.0% (0) | 10 | fabiola.jackson@bikes.shop, mireya.copeland@bikes.shop, genna.serrano@bikes.shop | - |
| `phone` 🔑 *(PK)* | `str` | 0.0% (0) | 10 | (831) 555-5554, (831) 555-5555, (831) 555-5556 | - |
| `active` | `int64` | 0.0% (0) | 1 | 1 | [1.0 to 1.0] |
| `store_id` | `int64` | 0.0% (0) | 3 | 1, 2, 3 | [1.0 to 3.0] |
| `manager_id` | `float64` | 10.0% (1) | 5 | 1.0, 2.0, 5.0 | [1.0 to 7.0] |


### Table: `products` (321 rows, 6 columns)

| Column | Data Type | Nulls (%) | Distinct Count | Sample Values | Range / Min-Max |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `product_id` 🔑 *(PK)* | `int64` | 0.0% (0) | 321 | 1, 2, 3 | [1.0 to 321.0] |
| `product_name` | `str` | 0.0% (0) | 291 | Trek 820 - 2016, Ritchey Timberwolf Frameset - 2016, Surly Wednesday Frameset - 2016 | - |
| `brand_id` | `int64` | 0.0% (0) | 9 | 9, 5, 8 | [1.0 to 9.0] |
| `category_id` | `int64` | 0.0% (0) | 7 | 6, 5, 4 | [1.0 to 7.0] |
| `model_year` | `int64` | 0.0% (0) | 4 | 2016, 2017, 2018 | [2016.0 to 2019.0] |
| `list_price` | `float64` | 0.0% (0) | 106 | 379.99, 749.99, 999.99 | [89.99 to 11999.99] |


### Table: `orders` (1,615 rows, 8 columns)

| Column | Data Type | Nulls (%) | Distinct Count | Sample Values | Range / Min-Max |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `order_id` 🔑 *(PK)* | `int64` | 0.0% (0) | 1615 | 1, 2, 3 | [1.0 to 1615.0] |
| `customer_id` | `int64` | 0.0% (0) | 1445 | 259, 1212, 523 | [1.0 to 1445.0] |
| `order_status` | `int64` | 0.0% (0) | 4 | 4, 3, 2 | [1.0 to 4.0] |
| `order_date` | `datetime64[us]` | 0.0% (0) | 725 | 2016-01-01 00:00:00, 2016-01-02 00:00:00, 2016-01-03 00:00:00 | [2016-01-01 00:00:00 to 2018-12-28 00:00:00] |
| `required_date` | `datetime64[us]` | 0.0% (0) | 734 | 2016-01-03 00:00:00, 2016-01-04 00:00:00, 2016-01-05 00:00:00 | [2016-01-03 00:00:00 to 2018-12-28 00:00:00] |
| `shipped_date` | `str` | 10.53% (170) | 676 | 2016-01-03, 2016-01-05, 2016-01-06 | - |
| `store_id` | `int64` | 0.0% (0) | 3 | 1, 2, 3 | [1.0 to 3.0] |
| `staff_id` | `int64` | 0.0% (0) | 6 | 2, 6, 7 | [2.0 to 9.0] |


### Table: `order_items` (4,722 rows, 6 columns)

| Column | Data Type | Nulls (%) | Distinct Count | Sample Values | Range / Min-Max |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `order_id` | `int64` | 0.0% (0) | 1615 | 1, 2, 3 | [1.0 to 1615.0] |
| `item_id` | `int64` | 0.0% (0) | 5 | 1, 2, 3 | [1.0 to 5.0] |
| `product_id` | `int64` | 0.0% (0) | 307 | 20, 8, 10 | [2.0 to 315.0] |
| `quantity` | `int64` | 0.0% (0) | 2 | 1, 2 | [1.0 to 2.0] |
| `list_price` | `float64` | 0.0% (0) | 104 | 599.99, 1799.99, 1549.0 | [89.99 to 11999.99] |
| `discount` | `float64` | 0.0% (0) | 4 | 0.2, 0.07, 0.05 | [0.05 to 0.2] |


### Table: `customers` (1,445 rows, 9 columns)

| Column | Data Type | Nulls (%) | Distinct Count | Sample Values | Range / Min-Max |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `customer_id` 🔑 *(PK)* | `int64` | 0.0% (0) | 1445 | 1, 2, 3 | [1.0 to 1445.0] |
| `first_name` | `str` | 0.0% (0) | 1265 | Debra, Kasha, Tameka | - |
| `last_name` | `str` | 0.0% (0) | 753 | Burks, Todd, Fisher | - |
| `phone` | `str` | 87.68% (1267) | 179 | (916) 381-6003, (716) 986-3359, (516) 583-7761 | - |
| `email` 🔑 *(PK)* | `str` | 0.0% (0) | 1445 | debra.burks@yahoo.com, kasha.todd@yahoo.com, tameka.fisher@aol.com | - |
| `street` 🔑 *(PK)* | `str` | 0.0% (0) | 1445 | 9273 Thorne Ave. , 910 Vine Street , 769C Honey Creek St.  | - |
| `city` | `str` | 0.0% (0) | 195 | Orchard Park, Campbell, Redondo Beach | - |
| `state` | `str` | 0.0% (0) | 3 | NY, CA, TX | - |
| `zip_code` | `int64` | 0.0% (0) | 195 | 14127, 95008, 90278 | [10002.0 to 95993.0] |


### Table: `categories` (7 rows, 2 columns)

| Column | Data Type | Nulls (%) | Distinct Count | Sample Values | Range / Min-Max |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `category_id` 🔑 *(PK)* | `int64` | 0.0% (0) | 7 | 1, 2, 3 | [1.0 to 7.0] |
| `category_name` 🔑 *(PK)* | `str` | 0.0% (0) | 7 | Children Bicycles, Comfort Bicycles, Cruisers Bicycles | - |


### Table: `brands` (9 rows, 2 columns)

| Column | Data Type | Nulls (%) | Distinct Count | Sample Values | Range / Min-Max |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `brand_id` 🔑 *(PK)* | `int64` | 0.0% (0) | 9 | 1, 2, 3 | [1.0 to 9.0] |
| `brand_name` 🔑 *(PK)* | `str` | 0.0% (0) | 9 | Electra, Haro, Heller | - |

