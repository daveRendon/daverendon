$key = $env:WEATHER_API_KEY
$cityId = "5809844"  # Seattle, US

# Emoji mapping based on OpenWeatherMap "weather condition codes"
$emojis = @{
    "01d" = "☀️"   # clear sky (day)
    "01n" = "🌙"   # clear sky (night)
    "02d" = "🌤"   # few clouds (day)
    "02n" = "☁️"   # few clouds (night)
    "03d" = "☁️"   # scattered clouds
    "03n" = "☁️"
    "04d" = "☁️"   # broken clouds
    "04n" = "☁️"
    "09d" = "🌧"   # shower rain
    "09n" = "🌧"
    "10d" = "🌦"   # rain (day)
    "10n" = "🌧"   # rain (night)
    "11d" = "⛈"   # thunderstorm
    "11n" = "⛈"
    "13d" = "❄️"   # snow
    "13n" = "❄️"
    "50d" = "🌫"   # mist
    "50n" = "🌫"
}

# OpenWeatherMap API URL (using current weather data)
$url = "http://api.openweathermap.org/data/2.5/weather?id=$cityId&appid=$key&units=imperial"
$r = Invoke-RestMethod $url

# Extract temperature and weather info
$degF = [math]::Round($r.main.temp)
$degC = [math]::Round((($degF - 32) / 1.8))

$iconCode = $r.weather[0].icon  # e.g., "01d", "10n"
$icon = $emojis[$iconCode]

# Same logic as before
$psTime = (Get-Date).year - (Get-Date "7/1/2013").year
$todayDay = (Get-Date).DayOfWeek

# Load and replace template placeholders
$data = Get-Content -Raw ./template.svg

$data = $data.Replace("{degF}", $degF)
$data = $data.Replace("{degC}", $degC)
$data = $data.Replace("{weatherEmoji}", $icon)
$data = $data.Replace("{psTime}", $psTime)
$data = $data.Replace("{todayDay}", $todayDay)

# Output
$data | Set-Content -Encoding utf8 ./chat.svg
