CREATE TABLE IF NOT EXISTS dashboard (
id INTEGER,
version INTEGER,
slug TEXT,
title TEXT,
data TEXT,
org_id INTEGER,
created DATETIME,
updated DATETIME,
updated_by INTEGER,
created_by INTEGER,
gnet_id INTEGER,
plugin_id TEXT,
folder_id INTEGER,
is_folder INTEGER,
has_acl INTEGER,
uid TEXT,
is_public INTEGER,
folder_uid TEXT
)

INSERT INTO dashboard VALUES (3, 6, 'gazes', 'Gāzes', b'{"annotations":{"list":[{"$$hashKey":"object:724","builtIn":1,"datasource":{"type":"datasource","uid":"grafana"},"enable":true,"hide":true,"iconColor":"rgba(0, 211, 255, 1)","name":"Annotations \\u0026 Alerts","type":"dashboard"}]},"editable":true,"fiscalYearStartMonth":0,"graphTooltip":0,"id":3,"links":[],"liveNow":false,"panels":[{"datasource":{"type":"mysql","uid":"000000001"},"description":"","fieldConfig":{"defaults":{"color":{"mode":"thresholds"},"custom":{"axisBorderShow":false,"axisCenteredZero":false,"axisColorMode":"text","axisLabel":"","axisPlacement":"auto","barAlignment":0,"drawStyle":"line","fillOpacity":10,"gradientMode":"scheme","hideFrom":{"legend":false,"tooltip":false,"viz":false},"insertNulls":false,"lineInterpolation":"linear","lineWidth":1,"pointSize":5,"scaleDistribution":{"type":"linear"},"showPoints":"never","spanNulls":false,"stacking":{"group":"A","mode":"none"},"thresholdsStyle":{"mode":"off"}},"links":[],"mappings":[],"thresholds":{"mode":"absolute","steps":[{"color":"green","value":null},{"color":"blue","value":600},{"color":"orange","value":1000},{"color":"dark-red","value":2500}]},"unit":"short"},"overrides":[]},"gridPos":{"h":9,"w":12,"x":0,"y":0},"id":2,"options":{"legend":{"calcs":[],"displayMode":"list","placement":"bottom","showLegend":true},"tooltip":{"mode":"multi","sort":"none"}},"pluginVersion":"10.3.0-pre","targets":[{"datasource":{"type":"mysql","uid":"000000001"},"editorMode":"code","format":"time_series","group":[],"metricColumn":"none","rawQuery":true,"rawSql":"SELECT\\n  time AS \\"time\\",\\n  `1` AS \\"CO2 ekvivalents ppm\\"\\nFROM s_2\\nWHERE\\n  $__timeFilter(time)\\nORDER BY time","refId":"A","select":[[{"params":["`1`"],"type":"column"}]],"sql":{"columns":[{"parameters":[],"type":"function"}],"groupBy":[{"property":{"type":"string"},"type":"groupBy"}],"limit":50},"table":"s_2","timeColumn":"time","timeColumnType":"datetime","where":[{"name":"$__timeFilter","params":[],"type":"macro"}]}],"type":"timeseries"}],"refresh":"","schemaVersion":39,"tags":[],"templating":{"list":[]},"time":{"from":"now-6h","to":"now"},"timepicker":{"refresh_intervals":["5s","10s","30s","1m","5m","15m","30m","1h","2h","1d"]},"timezone":"","title":"G\xc4\x81zes","uid":"cX1l5UvIz","version":6,"weekStart":""}', 1, '2023-12-15 02:23:24', '2023-12-26 05:01:51', 1, 1, 0, '', 0, 0, 0, 'cX1l5UvIz', 0, None);
