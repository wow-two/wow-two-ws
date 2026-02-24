# Haven Currency SDK — Specification

## Overview

.NET SDK for working with CBU (Central Bank of Uzbekistan) exchange rates. Wraps the public CBU API and provides strongly-typed currency models, conversion utilities, and caching.

## Data Source

- **API:** `https://cbu.uz/uz/arkhiv-kursov-valyut/json/`
- **Format:** JSON array of currency objects
- **Update frequency:** Daily (published each business day)
- **Base currency:** UZS (Uzbek Som) — all rates are quoted as `1 foreign unit = X UZS`
- **Total currencies:** 74 currencies + 1 SDR (XDR) = 75 entries

## API Response Schema

Each entry in the JSON array:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | int | Internal CBU identifier | `69` |
| `Code` | string | ISO 4217 numeric code | `"840"` |
| `Ccy` | string | ISO 4217 alpha code | `"USD"` |
| `CcyNm_RU` | string | Currency name in Russian | `"Доллар США"` |
| `CcyNm_UZ` | string | Currency name in Uzbek (Latin) | `"AQSH dollari"` |
| `CcyNm_UZC` | string | Currency name in Uzbek (Cyrillic) | `"АҚШ доллари"` |
| `CcyNm_EN` | string | Currency name in English | `"US Dollar"` |
| `Nominal` | string | Unit count for rate (usually `"1"`, sometimes `"10"`) | `"1"` |
| `Rate` | string | Exchange rate per Nominal units in UZS | `"12212.79"` |
| `Diff` | string | Change from previous day | `"43.38"` |
| `Date` | string | Rate date (`dd.MM.yyyy`) | `"23.02.2026"` |

### Nominal field

Some currencies quote rates per 10 units (not 1):

| Ccy | Nominal | Meaning |
|-----|---------|---------|
| IDR | 10 | 10 Indonesian Rupiah = 7.24 UZS |
| IRR | 10 | 10 Iranian Rial = 0.09 UZS |
| VND | 10 | 10 Vietnamese Dong = 4.70 UZS |

All other currencies have `Nominal = 1`.

## Currency List (75 entries)

### Major Currencies

| # | Code | Ccy | English Name | Sample Rate |
|---|------|-----|-------------|-------------|
| 1 | 840 | USD | US Dollar | 12,212.79 |
| 2 | 978 | EUR | Euro | 14,411.09 |
| 3 | 826 | GBP | Pound Sterling | 16,493.37 |
| 4 | 392 | JPY | Japan Yen | 78.89 |
| 5 | 756 | CHF | Swiss Franc | 15,795.12 |
| 6 | 156 | CNY | Yuan Renminbi | 1,767.74 |
| 7 | 643 | RUB | Russian Ruble | 159.52 |

### Regional / CIS Currencies

| # | Code | Ccy | English Name |
|---|------|-----|-------------|
| 8 | 051 | AMD | Armenian Dram |
| 9 | 944 | AZN | Azerbaijan Manat |
| 10 | 933 | BYN | Belarusian Ruble |
| 11 | 981 | GEL | Georgian Lari |
| 12 | 398 | KZT | Kazakhstan Tenge |
| 13 | 417 | KGS | Kyrgyzstan Som |
| 14 | 972 | TJS | Tajikistan Somoni |
| 15 | 934 | TMT | Turkmenistan New Manat |
| 16 | 980 | UAH | Ukrainian Hryvnia |

### Middle East & Gulf

| # | Code | Ccy | English Name |
|---|------|-----|-------------|
| 17 | 784 | AED | UAE Dirham |
| 18 | 048 | BHD | Bahraini Dinar |
| 19 | 368 | IQD | Iraqi Dinar |
| 20 | 364 | IRR | Iranian Rial |
| 21 | 376 | ILS | New Israeli Sheqel |
| 22 | 400 | JOD | Jordanian Dinar |
| 23 | 414 | KWD | Kuwaiti Dinar |
| 24 | 422 | LBP | Lebanese Pound |
| 25 | 512 | OMR | Rial Omani |
| 26 | 634 | QAR | Qatari Rial |
| 27 | 682 | SAR | Saudi Riyal |
| 28 | 760 | SYP | Syrian Pound |
| 29 | 886 | YER | Yemeni Rial |

### Asia-Pacific

| # | Code | Ccy | English Name |
|---|------|-----|-------------|
| 30 | 036 | AUD | Australian Dollar |
| 31 | 050 | BDT | Bangladesh Taka |
| 32 | 096 | BND | Brunei Dollar |
| 33 | 344 | HKD | Hong Kong Dollar |
| 34 | 360 | IDR | Rupiah |
| 35 | 356 | INR | Indian Rupee |
| 36 | 116 | KHR | Riel (Cambodia) |
| 37 | 410 | KRW | Korean Republic Won |
| 38 | 418 | LAK | Lao Kip |
| 39 | 458 | MYR | Malaysian Ringgit |
| 40 | 104 | MMK | Kyat (Myanmar) |
| 41 | 496 | MNT | Tugrik (Mongolia) |
| 42 | 554 | NZD | New Zealand Dollar |
| 43 | 608 | PHP | Philippine Piso |
| 44 | 586 | PKR | Pakistan Rupee |
| 45 | 702 | SGD | Singapore Dollar |
| 46 | 764 | THB | Baht |
| 47 | 704 | VND | Dong (Vietnam) |

### Europe (non-EUR)

| # | Code | Ccy | English Name |
|---|------|-----|-------------|
| 48 | 975 | BGN | Bulgarian Lev |
| 49 | 203 | CZK | Czech Koruna |
| 50 | 208 | DKK | Danish Krone |
| 51 | 348 | HUF | Hungarian Forint |
| 52 | 352 | ISK | Iceland Krona |
| 53 | 498 | MDL | Moldovan Leu |
| 54 | 578 | NOK | Norwegian Krone |
| 55 | 985 | PLN | Polish Zloty |
| 56 | 946 | RON | Romanian Leu |
| 57 | 941 | RSD | Serbian Dinar |
| 58 | 752 | SEK | Swedish Krona |
| 59 | 949 | TRY | Turkish Lira |

### Americas

| # | Code | Ccy | English Name |
|---|------|-----|-------------|
| 60 | 032 | ARS | Argentine Peso |
| 61 | 986 | BRL | Brazilian Real |
| 62 | 124 | CAD | Canadian Dollar |
| 63 | 192 | CUP | Cuban Peso |
| 64 | 484 | MXN | Mexican Peso |
| 65 | 858 | UYU | Peso Uruguayo |
| 66 | 928 | VES | Bolívar (Venezuela) |

### Africa

| # | Code | Ccy | English Name |
|---|------|-----|-------------|
| 67 | 012 | DZD | Algerian Dinar |
| 68 | 818 | EGP | Egyptian Pound |
| 69 | 434 | LYD | Libyan Dinar |
| 70 | 504 | MAD | Moroccan Dirham |
| 71 | 938 | SDG | Sudanese Pound |
| 72 | 788 | TND | Tunisian Dinar |
| 73 | 710 | ZAR | Rand (South Africa) |

### Other

| # | Code | Ccy | English Name |
|---|------|-----|-------------|
| 74 | 971 | AFN | AF Afghani |
| 75 | 960 | XDR | SDR (IMF Special Drawing Rights) |

## SDK Architecture

### Project Structure

```
Haven.Currencies/
├── Haven.Currencies.csproj
├── Models/
│   ├── Currency.cs              # Core currency model
│   ├── ExchangeRate.cs          # Rate with metadata
│   └── ConversionResult.cs      # Conversion output
├── Enums/
│   └── CurrencyCode.cs          # Strongly-typed enum (75 values)
├── Client/
│   ├── ICbuClient.cs            # Interface for CBU API
│   └── CbuClient.cs             # HttpClient-based implementation
├── Services/
│   ├── ICurrencyService.cs      # High-level service interface
│   └── CurrencyService.cs       # Conversion, lookup, caching
├── Caching/
│   ├── IRateCache.cs            # Cache interface
│   └── InMemoryRateCache.cs     # Default in-memory cache
├── Configuration/
│   └── CurrencyOptions.cs       # SDK configuration
├── Extensions/
│   └── ServiceCollectionExtensions.cs  # DI registration
└── Exceptions/
    ├── CbuApiException.cs       # API call failures
    └── CurrencyNotFoundException.cs
```

### Target Framework

- **.NET 9** (aligned with Haven backend services)
- **NuGet dependencies:** `System.Text.Json`, `Microsoft.Extensions.Http`, `Microsoft.Extensions.Caching.Memory`

## Models

### Currency

```csharp
public record Currency
{
    public int Id { get; init; }
    public string NumericCode { get; init; }     // "840"
    public CurrencyCode Code { get; init; }       // CurrencyCode.USD
    public string NameRu { get; init; }
    public string NameUz { get; init; }
    public string NameUzCyrillic { get; init; }
    public string NameEn { get; init; }
}
```

### ExchangeRate

```csharp
public record ExchangeRate
{
    public CurrencyCode Code { get; init; }
    public int Nominal { get; init; }             // 1 or 10
    public decimal Rate { get; init; }            // UZS per Nominal units
    public decimal RatePerUnit { get; init; }     // Rate / Nominal (normalized)
    public decimal Diff { get; init; }
    public DateOnly Date { get; init; }
    public Currency Currency { get; init; }
}
```

### ConversionResult

```csharp
public record ConversionResult
{
    public decimal Amount { get; init; }
    public CurrencyCode From { get; init; }
    public CurrencyCode To { get; init; }
    public decimal Result { get; init; }
    public decimal Rate { get; init; }            // Effective cross-rate
    public DateOnly RateDate { get; init; }
}
```

### CurrencyCode Enum

```csharp
public enum CurrencyCode
{
    AED, AFN, AMD, ARS, AUD, AZN,
    BDT, BGN, BHD, BND, BRL, BYN,
    CAD, CHF, CNY, CUP, CZK,
    DKK, DZD,
    EGP, EUR,
    GBP, GEL,
    HKD, HUF,
    IDR, ILS, INR, IQD, IRR, ISK,
    JOD, JPY,
    KGS, KHR, KRW, KWD, KZT,
    LAK, LBP, LYD,
    MAD, MDL, MMK, MNT, MXN, MYR,
    NOK, NZD,
    OMR,
    PHP, PKR, PLN,
    QAR,
    RON, RSD, RUB,
    SAR, SDG, SEK, SGD, SYP,
    THB, TJS, TMT, TND, TRY,
    UAH, USD, UYU,
    VES, VND,
    XDR,
    YER,
    ZAR
}
```

## Service Interface

```csharp
public interface ICurrencyService
{
    // Fetch latest rates
    Task<IReadOnlyList<ExchangeRate>> GetAllRatesAsync(CancellationToken ct = default);
    Task<ExchangeRate> GetRateAsync(CurrencyCode code, CancellationToken ct = default);

    // Fetch rates for specific date
    Task<IReadOnlyList<ExchangeRate>> GetRatesForDateAsync(DateOnly date, CancellationToken ct = default);
    Task<ExchangeRate> GetRateForDateAsync(CurrencyCode code, DateOnly date, CancellationToken ct = default);

    // Conversion
    Task<ConversionResult> ConvertAsync(decimal amount, CurrencyCode from, CurrencyCode to, CancellationToken ct = default);

    // UZS shortcuts
    Task<decimal> ToUzsAsync(decimal amount, CurrencyCode from, CancellationToken ct = default);
    Task<decimal> FromUzsAsync(decimal uzsAmount, CurrencyCode to, CancellationToken ct = default);

    // Metadata
    Currency GetCurrencyInfo(CurrencyCode code);
    IReadOnlyList<Currency> GetAllCurrencies();
}
```

## Configuration

```csharp
public class CurrencyOptions
{
    public string BaseUrl { get; set; } = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/";
    public TimeSpan CacheDuration { get; set; } = TimeSpan.FromMinutes(60);
    public int HttpTimeoutSeconds { get; set; } = 10;
    public int RetryCount { get; set; } = 3;
}
```

## DI Registration

```csharp
// Program.cs
builder.Services.AddHavenCurrencies(options =>
{
    options.CacheDuration = TimeSpan.FromMinutes(30);
});
```

Extension method:

```csharp
public static IServiceCollection AddHavenCurrencies(
    this IServiceCollection services,
    Action<CurrencyOptions>? configure = null)
{
    var options = new CurrencyOptions();
    configure?.Invoke(options);

    services.AddSingleton(options);
    services.AddHttpClient<ICbuClient, CbuClient>(/* timeout, retry policy */);
    services.AddSingleton<IRateCache, InMemoryRateCache>();
    services.AddScoped<ICurrencyService, CurrencyService>();

    return services;
}
```

## CBU API Endpoints

| Purpose | URL Pattern |
|---------|-------------|
| Latest rates | `GET /uz/arkhiv-kursov-valyut/json/` |
| Specific currency (latest) | `GET /uz/arkhiv-kursov-valyut/json/USD/` |
| Specific date | `GET /uz/arkhiv-kursov-valyut/json/all/{date}/` |
| Specific currency + date | `GET /uz/arkhiv-kursov-valyut/json/USD/{date}/` |

Date format in URL: `yyyy-MM-dd`

## Conversion Logic

All CBU rates are `foreign → UZS`. Cross-currency conversion:

```
// Foreign → UZS
uzs = amount * (rate / nominal)

// UZS → Foreign
foreign = uzsAmount / (rate / nominal)

// Foreign A → Foreign B (cross-rate via UZS)
uzs = amount * (rateA / nominalA)
result = uzs / (rateB / nominalB)
```

## Caching Strategy

- **Key:** `rates:{date}` (date string or `"latest"`)
- **Default TTL:** 60 minutes for latest, permanent for historical dates
- **Invalidation:** Latest cache invalidated on next business day
- **Thread safety:** `ConcurrentDictionary` + `SemaphoreSlim` for fetch dedup

## Error Handling

| Scenario | Exception |
|----------|-----------|
| CBU API unreachable / 5xx | `CbuApiException` |
| Unknown currency code | `CurrencyNotFoundException` |
| Invalid date range | `ArgumentOutOfRangeException` |
| Rate data missing for date | `CbuApiException("No rates for date")` |

## Integration with Haven

This SDK replaces the current `ExchangeRateService` in `Haven.Settings` for CBU rate fetching. The `exchange_rates` table and `price_usd` trigger in Supabase remain — the SDK feeds into that pipeline.

### Usage in Haven.Settings

```csharp
// ExchangeRateBackgroundService.cs
var usdRate = await _currencyService.GetRateAsync(CurrencyCode.USD);
await _repository.UpsertRateAsync("USD/UZS", usdRate.RatePerUnit);
```

## Testing

- **Unit tests:** Mock `ICbuClient`, test conversion math (especially Nominal=10 currencies)
- **Integration tests:** Hit real CBU API with rate limiting
- **Edge cases:** Weekend dates (no new rates), Nominal=10 normalization, XDR handling
