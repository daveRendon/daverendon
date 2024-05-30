$key = $env:WEATHER_API_KEY
$location = "Seattle"

$emojis = @{
    1  = "☀️"
    2  = "☀️"
    3  = "🌤"
    4  = "🌤"
    5  = "🌤"
    6  = "🌥"
    7  = "☁️"
    8  = "☁️"
    11 = "🌫"
    12 = "🌧"
    13 = "🌦"
    14 = "🌦"
    15 = "⛈"
    16 = "⛈"
    17 = "🌦"
    18 = "🌧"
    19 = "🌨"
    20 = "🌨"
    21 = "🌨"
    22 = "❄️"
    23 = "❄️"
    24 = "🌧"
    25 = "🌧"
    26 = "🌧"
    29 = "🌧"
    30 = "🌫"
    31 = "🥵"
    32 = "🥶"
}

$url = "https://api.openweathermap.org/data/2.5/weather?q=$location&appid=96ef9dc6a7a0c941aea8f8afbcf0a1ba"
$r = Invoke-RestMethod $url

$temp_kelvin = $r.main.temp
$degC = [math]::Round($temp_kelvin - 273.15)
$icon = $emojis[[int]$r.weather[0].id]
$todayDay = (Get-Date).DayOfWeek

$data = Get-Content -Raw ./template.svg

$data = $data.replace("{degC}", $degC)
$data = $data.replace("{weatherEmoji}", $icon)
$data = $data.replace("{todayDay}", $todayDay)

$data | Set-Content -Encoding utf8 ./chat.svg
