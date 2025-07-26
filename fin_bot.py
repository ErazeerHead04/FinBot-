
import pandas as pd
import re

# ----- Load & clean data -----
df = pd.read_csv('10K report.csv', thousands=',')
df.columns = [c.strip() for c in df.columns]

COMPANIES = df['Company'].unique().tolist()
FIELDS = {
    'revenue':     'T Revenue',
    'net income':  'Net income',
    'assets':      'T Assests',
    'liabilities': 'T Liabilities',
    'cash flow':   'Cash Flow (Operation)'
}

# field variants
FIELD_ALIASES = {}
for k in FIELDS:
    FIELD_ALIASES[k] = k
    FIELD_ALIASES[k.replace(' ', '')] = k
    if k.endswith('s'):
        FIELD_ALIASES[k[:-1]] = k
    else:
        FIELD_ALIASES[k + 's'] = k

# stat keywords
STAT_KEYWORDS = {
    'max':     'max',
    'min':     'min',
    'minimum': 'min',
    'average': 'mean',
    'mean':    'mean',
    'closest': 'closest'
}

YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")

def parse_field(text):
    t = text.lower().replace('-', ' ')
    for a, k in FIELD_ALIASES.items():
        if a in t:
            return k
    return None

def parse_company(text):
    t = text.lower()
    for c in COMPANIES:
        if c.lower() in t:
            return c
    return None

def parse_year(text):
    m = YEAR_RE.search(text)
    return int(m.group()) if m else None

def parse_stat(text):
    t = text.lower()
    for w, s in STAT_KEYWORDS.items():
        if w in t:
            return s
    return None

def get_cell(company, field, year):
    sub = df[(df.Company==company)&(df.Year==year)]
    return None if sub.empty else sub.iloc[0][FIELDS[field]]

def compute_stats(company, field):
    sub = df[df.Company==company].sort_values('Year').reset_index(drop=True)
    if sub.empty:
        return None
    s    = sub[FIELDS[field]].astype(float)
    yrs  = sub['Year'].tolist()
    mean = s.mean()
    i_min = s.idxmin()
    i_max = s.idxmax()
    i_cl  = (s - mean).abs().idxmin()
    return {
        'mean':    mean,
        'min':     (s.iloc[i_min], yrs[i_min]),
        'max':     (s.iloc[i_max], yrs[i_max]),
        'closest': (s.iloc[i_cl],  yrs[i_cl])
    }

print("Welcome to FinBot! 🤖")
print("I show financial performance of Microsoft, Tesla, and Apple for the last three fiscal years using SEC 10‑K filings.")
print("Ask for a specific data point (e.g. “revenue of Apple in 2022”),")
print("or a series stat (e.g. “max revenue of Tesla”).")
print("Fields: Revenue, Net income, Assets, Liabilities, Cash flow")
print("Stats: max, min, average, closest\n")

while True:
    # context for this request
    field   = company = year = stat = None

    # keep asking until we can answer
    while True:
        text = input("You: ").strip()
        if text.lower() == 'exit':
            print("FinanceBot: Goodbye! 👋")
            exit()

        # update context
        field   = field   or parse_field(text)
        company = company or parse_company(text)
        year    = year    or parse_year(text)
        stat    = stat    or parse_stat(text)

        if not any((field, company, year, stat)):
            print("FinanceBot: I am a fin bot. I can only give you information from 10‑K filings.")
            #Go back to waiting for a fresh request
            break
        # decide mode
        if stat:
            # series stat: need stat, field, company
            missing = []
            if not stat:    missing.append("stat (max/min/average/closest)")
            if not field:   missing.append("field")
            if not company: missing.append("company")
            if missing:
                print("FinanceBot: I need:", ", ".join(missing))
                continue
            # answer series stat
            stats = compute_stats(company, field)
            if not stats:
                print(f"FinanceBot: No data for {company}.")
            else:
                if stat == 'mean':
                    print(f"FinanceBot: Average {field} for {company} is {stats['mean']:,}.")
                else:
                    val, yr = stats[stat]
                    print(f"FinanceBot: {stat.title()} {field} for {company} is {int(val):,} (in {yr}).")
            break

        elif year:
            # single-year lookup: need field, company, year
            missing = []
            if not field:   missing.append("field")
            if not company: missing.append("company")
            if not year:    missing.append("year")
            if missing:
                print("FinanceBot: I need:", ", ".join(missing))
                continue
            # answer cell
            val = get_cell(company, field, year)
            if val is None:
                print(f"FinanceBot: No data for {company} {field} in {year}.")
            else:
                print(f"FinanceBot: {field.title()} for {company} in {year} was {int(val):,}.")
            break

        else:
            # neither stat nor year yet: need at least one plus field+company
            missing = []
            if not field:   missing.append("field")
            if not company: missing.append("company")
            missing.append("stat or year")
            print("FinanceBot: I need:", ", ".join(missing))
            continue

    print()  # blank line before next request
