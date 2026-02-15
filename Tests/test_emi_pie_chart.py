import pytest
from playwright.sync_api import Page, Browser

@pytest.mark.parametrize("loan_amount,interest,term", [
    ("2500000", "10", "10"),
    ("5000000", "8.5", "15"),
])
def test_emi_pie_chart(browser: Browser, loan_amount, interest, term):

    page: Page = browser.new_page()

    page.goto("https://emicalculator.net/")
    page.wait_for_load_state("networkidle")

    # page.evaluate("() => window.moveTo(0,0); window.resizeTo(screen.width, screen.height);")

    home_loan_tab = page.locator("#home-loan")
    home_loan_tab.wait_for(state="visible", timeout=10000)
    home_loan_tab.click()

    page.locator("#loanamount").wait_for(state="visible", timeout=10000)
    page.fill("#loanamount", loan_amount)
    page.fill("#loaninterest", interest)
    page.fill("#loanterm", term)

    pie_chart = page.locator("#emipiechart")
    assert pie_chart.is_visible(), "EMI Pie Chart is not visible!"

    pie_labels_locator = page.locator("g.highcharts-data-labels tspan")
    pie_labels_locator.first.scroll_into_view_if_needed()
    pie_labels_locator.first.wait_for(state="visible", timeout=5000)

    labels_text = [label.strip() for label in pie_labels_locator.all_text_contents()]
    print(f"Pie chart labels for loan {loan_amount}, interest {interest}, Tenure {term}: {labels_text}")

    labels_values = [float(label.replace("%", "")) for label in labels_text]
    assert all(value > 0 for value in labels_values), "Some pie chart values are zero or negative!"

    print(f"All pie chart values are greater than zero for loan {loan_amount}, interest {interest}, Tenure {term}")

    page.close()
