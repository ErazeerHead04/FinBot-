#  FinanceBot – Financial Intelligence Assistant

**FinanceBot** is a terminal-based chatbot that interprets natural language queries to provide structured financial insights from SEC 10-K filings of **Microsoft**, **Apple**, and **Tesla** over the last three fiscal years.

This project combines financial research, data analysis, and basic NLP to deliver an intelligent conversational tool for exploring company performance.

---

##  Project Overview

- Conducted financial research on Microsoft, Apple, and Tesla using SEC 10-K filings.
- Cleaned and structured financial data into a CSV format.
- Built a terminal-based chatbot to answer user queries about:
  - Revenue
  - Net income
  - Assets
  - Liabilities
  - Operational cash flow
- Created a final analytical report with graphs and business insights.

---

##  Technologies Used

- **Python** – core programming language
- **pandas** & **numpy** – data wrangling and computation
- **matplotlib** – visualizations used in report
- **re (Regular Expressions)** – for date and pattern parsing
- **Basic NLP techniques** – intent detection via keyword matching

---

##  Key Features

- Understands natural language queries like:
  - "What was Apple’s revenue in 2022?"
  - "Max net income of Tesla"
  - "Average assets for Microsoft"
- Returns both:
  - Specific year values
  - Aggregate statistics (`max`, `min`, `average`, `closest`)
- Handles data validation and clarifies missing query parts

---

##  Project Files

```text
.
├── finbot.py              # Main chatbot logic
├── 10K report.csv         # Structured financial data
├── Final Report.html      # Business and financial analysis report
```

---

##  How to Run

From your terminal:

```bash
python finbot.py
```

Example interaction:

```
You: average assets of Tesla
FinanceBot: Average assets for Tesla is 85,114.

You: Apple net income 2022
FinanceBot: Net income for Apple in 2022 was 99,803.
```

Use `exit` to quit.

---

##  Final Report

The `Final Report.html` file includes:
- Graphs and charts comparing performance
- Trend analysis for each company
- Key financial insights and commentary

---


