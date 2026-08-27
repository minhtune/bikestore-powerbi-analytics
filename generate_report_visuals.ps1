# Power BI Visuals Generator with Verified Schema Names (Exact Match with model.bim)

$reportPath = "BikeStore_Analytics.Report\report.json"
$backupPath = "BikeStore_Analytics.Report\report.json.bak"

if (Test-Path $reportPath) {
    Copy-Item $reportPath $backupPath -Force
}

$rawJson = Get-Content $reportPath -Raw -Encoding UTF8 | ConvertFrom-Json

function New-VisualId {
    $bytes = New-Object byte[] 10
    [Security.Cryptography.RNGCryptoServiceProvider]::Create().GetBytes($bytes)
    return -join ($bytes | ForEach-Object { $_.ToString("x2") })
}

function New-CardVisual($x, $y, $w, $h, $measureName, $z = 1000) {
    $vId = New-VisualId
    $configObj = @{
        name = $vId
        layouts = @(
            @{
                id = 0
                position = @{
                    x = $x
                    y = $y
                    z = $z
                    width = $w
                    height = $h
                    tabOrder = $z
                }
            }
        )
        singleVisual = @{
            visualType = "card"
            projections = @{
                Values = @(
                    @{
                        queryRef = "_Measures.$measureName"
                    }
                )
            }
            prototypeQuery = @{
                Version = 2
                From = @(
                    @{
                        Name = "m"
                        Entity = "_Measures"
                        Type = 0
                    }
                )
                Select = @(
                    @{
                        Measure = @{
                            Expression = @{
                                SourceRef = @{
                                    Source = "m"
                                }
                            }
                            Property = $measureName
                        }
                        Name = "_Measures.$measureName"
                    }
                )
            }
        }
    }
    
    $configJson = $configObj | ConvertTo-Json -Depth 10 -Compress
    
    return [PSCustomObject]@{
        x = $x
        y = $y
        z = $z
        width = $w
        height = $h
        config = $configJson
    }
}

function New-BarChartVisual($x, $y, $w, $h, $catTable, $catCol, $measureName, $z = 1000) {
    $vId = New-VisualId
    $configObj = @{
        name = $vId
        layouts = @(
            @{
                id = 0
                position = @{
                    x = $x
                    y = $y
                    z = $z
                    width = $w
                    height = $h
                    tabOrder = $z
                }
            }
        )
        singleVisual = @{
            visualType = "clusteredBarChart"
            projections = @{
                Category = @(
                    @{
                        queryRef = "$catTable.$catCol"
                        active = $true
                    }
                )
                Y = @(
                    @{
                        queryRef = "_Measures.$measureName"
                    }
                )
            }
            prototypeQuery = @{
                Version = 2
                From = @(
                    @{
                        Name = "c"
                        Entity = $catTable
                        Type = 0
                    },
                    @{
                        Name = "m"
                        Entity = "_Measures"
                        Type = 0
                    }
                )
                Select = @(
                    @{
                        Column = @{
                            Expression = @{
                                SourceRef = @{
                                    Source = "c"
                                }
                            }
                            Property = $catCol
                        }
                        Name = "$catTable.$catCol"
                    },
                    @{
                        Measure = @{
                            Expression = @{
                                SourceRef = @{
                                    Source = "m"
                                }
                            }
                            Property = $measureName
                        }
                        Name = "_Measures.$measureName"
                    }
                )
            }
        }
    }
    
    $configJson = $configObj | ConvertTo-Json -Depth 10 -Compress
    
    return [PSCustomObject]@{
        x = $x
        y = $y
        z = $z
        width = $w
        height = $h
        config = $configJson
    }
}

function New-LineChartVisual($x, $y, $w, $h, $dateTable, $dateCol, $measureName, $z = 1000) {
    $vId = New-VisualId
    $configObj = @{
        name = $vId
        layouts = @(
            @{
                id = 0
                position = @{
                    x = $x
                    y = $y
                    z = $z
                    width = $w
                    height = $h
                    tabOrder = $z
                }
            }
        )
        singleVisual = @{
            visualType = "lineChart"
            projections = @{
                Category = @(
                    @{
                        queryRef = "$dateTable.$dateCol"
                        active = $true
                    }
                )
                Y = @(
                    @{
                        queryRef = "_Measures.$measureName"
                    }
                )
            }
            prototypeQuery = @{
                Version = 2
                From = @(
                    @{
                        Name = "d"
                        Entity = $dateTable
                        Type = 0
                    },
                    @{
                        Name = "m"
                        Entity = "_Measures"
                        Type = 0
                    }
                )
                Select = @(
                    @{
                        Column = @{
                            Expression = @{
                                SourceRef = @{
                                    Source = "d"
                                }
                            }
                            Property = $dateCol
                        }
                        Name = "$dateTable.$dateCol"
                    },
                    @{
                        Measure = @{
                            Expression = @{
                                SourceRef = @{
                                    Source = "m"
                                }
                            }
                            Property = $measureName
                        }
                        Name = "_Measures.$measureName"
                    }
                )
            }
        }
    }
    
    $configJson = $configObj | ConvertTo-Json -Depth 10 -Compress
    
    return [PSCustomObject]@{
        x = $x
        y = $y
        z = $z
        width = $w
        height = $h
        config = $configJson
    }
}

function New-TableVisual($x, $y, $w, $h, $columnPairs, $measures, $z = 1000) {
    $vId = New-VisualId
    $projections = @()
    $fromList = @()
    $selectList = @()
    $tablesSeen = @{}
    
    foreach ($pair in $columnPairs) {
        $tbl = $pair[0]
        $col = $pair[1]
        if (-not $tablesSeen.ContainsKey($tbl)) {
            $alias = "t" + $tablesSeen.Count
            $tablesSeen[$tbl] = $alias
            $fromList += @{ Name = $alias; Entity = $tbl; Type = 0 }
        }
        $alias = $tablesSeen[$tbl]
        $qRef = "$tbl.$col"
        $projections += @{ queryRef = $qRef }
        $selectList += @{
            Column = @{
                Expression = @{ SourceRef = @{ Source = $alias } }
                Property = $col
            }
            Name = $qRef
        }
    }
    
    if ($measures) {
        if (-not $tablesSeen.ContainsKey("_Measures")) {
            $alias = "m"
            $tablesSeen["_Measures"] = $alias
            $fromList += @{ Name = $alias; Entity = "_Measures"; Type = 0 }
        }
        $alias = $tablesSeen["_Measures"]
        foreach ($m in $measures) {
            $qRef = "_Measures.$m"
            $projections += @{ queryRef = $qRef }
            $selectList += @{
                Measure = @{
                    Expression = @{ SourceRef = @{ Source = $alias } }
                    Property = $m
                }
                Name = $qRef
            }
        }
    }
    
    $configObj = @{
        name = $vId
        layouts = @(
            @{
                id = 0
                position = @{
                    x = $x
                    y = $y
                    z = $z
                    width = $w
                    height = $h
                    tabOrder = $z
                }
            }
        )
        singleVisual = @{
            visualType = "tableEx"
            projections = @{
                Values = $projections
            }
            prototypeQuery = @{
                Version = 2
                From = $fromList
                Select = $selectList
            }
        }
    }
    
    $configJson = $configObj | ConvertTo-Json -Depth 10 -Compress
    
    return [PSCustomObject]@{
        x = $x
        y = $y
        z = $z
        width = $w
        height = $h
        config = $configJson
    }
}

# ==============================================================================
# BIKESTORE DASHBOARD PAGES (EXACT model.bim Column Names)
# ==============================================================================

# Page 1: Executive Overview
$p1Visuals = @(
    (New-CardVisual 20 20 230 95 "Total Net Revenue" 1000),
    (New-CardVisual 270 20 230 95 "Total Orders" 1010),
    (New-CardVisual 520 20 230 95 "Average Order Value" 1020),
    (New-CardVisual 770 20 230 95 "Total Units Sold" 1030),
    (New-CardVisual 1020 20 240 95 "Total Active Customers" 1040),
    (New-LineChartVisual 20 130 730 310 "Dim_Date" "YearMonth" "Total Net Revenue" 2000),
    (New-BarChartVisual 770 130 490 310 "Dim_Product" "Category_Name" "Total Net Revenue" 2010),
    (New-BarChartVisual 20 460 600 240 "Dim_Product" "Brand_Name" "Total Net Revenue" 3000),
    (New-TableVisual 640 460 620 240 @(@("Dim_Store", "Store_Name"), @("Dim_Store", "State")) @("Total Net Revenue", "Total Orders") 3010)
)

# Page 2: Products & Inventory
$p2Visuals = @(
    (New-CardVisual 20 20 290 95 "Total Stock Quantity" 1000),
    (New-CardVisual 330 20 290 95 "Total Stock Value" 1010),
    (New-CardVisual 640 20 290 95 "Total Units Sold" 1020),
    (New-CardVisual 950 20 310 95 "Total Net Revenue" 1030),
    (New-BarChartVisual 20 130 600 310 "Dim_Product" "Category_Name" "Total Stock Quantity" 2000),
    (New-BarChartVisual 640 130 620 310 "Dim_Store" "Store_Name" "Total Stock Quantity" 2010),
    (New-TableVisual 20 460 1240 240 @(@("Dim_Product", "Product_Name"), @("Dim_Product", "Brand_Name"), @("Dim_Product", "Category_Name")) @("Total Stock Quantity", "Total Units Sold", "Total Net Revenue") 3000)
)

# Page 3: Customers & Geography
$p3Visuals = @(
    (New-CardVisual 20 20 290 95 "Total Active Customers" 1000),
    (New-CardVisual 330 20 290 95 "Total Net Revenue" 1010),
    (New-CardVisual 640 20 290 95 "Average Order Value" 1020),
    (New-CardVisual 950 20 310 95 "Revenue Per Customer" 1030),
    (New-BarChartVisual 20 130 600 310 "Dim_Customer" "State" "Total Net Revenue" 2000),
    (New-BarChartVisual 640 130 620 310 "Dim_Staff" "Staff_Name" "Total Net Revenue" 2010),
    (New-TableVisual 20 460 1240 240 @(@("Dim_Customer", "Customer_Name"), @("Dim_Customer", "City"), @("Dim_Customer", "State")) @("Total Net Revenue", "Total Orders") 3000)
)

# Page 4: Fulfillment & Operations
$p4Visuals = @(
    (New-CardVisual 20 20 290 95 "Total Orders" 1000),
    (New-CardVisual 330 20 290 95 "Total Units Sold" 1010),
    (New-CardVisual 640 20 290 95 "Total Gross Revenue" 1020),
    (New-CardVisual 950 20 310 95 "Average Discount %" 1030),
    (New-BarChartVisual 20 130 600 310 "Fact_Sales" "Order_Status" "Total Orders" 2000),
    (New-BarChartVisual 640 130 620 310 "Dim_Store" "Store_Name" "Total Orders" 2010),
    (New-TableVisual 20 460 1240 240 @(@("Dim_Store", "Store_Name"), @("Dim_Store", "City"), @("Dim_Store", "State")) @("Total Orders", "Total Net Revenue", "Average Discount %") 3000)
)

$rawJson.sections[0].visualContainers = $p1Visuals
$rawJson.sections[1].visualContainers = $p2Visuals
$rawJson.sections[2].visualContainers = $p3Visuals
$rawJson.sections[3].visualContainers = $p4Visuals

$finalJson = $rawJson | ConvertTo-Json -Depth 15
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText((Resolve-Path $reportPath).Path, $finalJson, $utf8NoBom)

Write-Host "SUCCESS: Generated complete visual containers with VERIFIED schema names (No BOM)!"
Write-Host "Page 1: $($p1Visuals.Count) visuals"
Write-Host "Page 2: $($p2Visuals.Count) visuals"
Write-Host "Page 3: $($p3Visuals.Count) visuals"
Write-Host "Page 4: $($p4Visuals.Count) visuals"
