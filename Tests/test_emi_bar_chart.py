
import re
from playwright.sync_api import Page, Browser

def set_slider_by_value(page, slider_selector, min_val, max_val, target_val):

    slider = page.locator(slider_selector)
    slider.wait_for(state="visible")

    box = slider.bounding_box()
    if not box:
        raise Exception(f"Bounding box not found for {slider_selector}")

    percentage = (target_val - min_val) / (max_val - min_val)

    target_x = box["x"] + box["width"] * percentage
    center_y = box["y"] + box["height"] / 2

    page.mouse.move(box["x"] + 1, center_y)  # start at left edge
    page.mouse.down()
    page.mouse.move(target_x, center_y)
    page.mouse.up()


def select_month(page, month_name):
    page.locator("span.month", has_text=month_name).click()


def test_validate_emi_bar_chart_with_sliders(browser: Browser):

        page: Page = browser.new_page()

        page.goto("https://emicalculator.net/")
        page.wait_for_load_state("networkidle")


        page.locator("#personal-loan").click()

        set_slider_by_value(page, "#loanamountslider",
                            min_val=0,
                            max_val=3000000,
                            target_val=1000000)

        set_slider_by_value(page, "#loaninterestslider",
                            min_val=5,
                            max_val=25,
                            target_val=12)

        set_slider_by_value(page, "#loantermslider",
                            min_val=0,
                            max_val=5,
                            target_val=5)

        page.wait_for_timeout(2000)

        page.locator("#startmonthyear").click()
        page.wait_for_selector(".datepicker-months")

        select_month(page, "Jul")

        bar_chart = page.locator("#emibarchart")
        bar_chart.wait_for(state="visible")

        assert bar_chart.is_visible(), "EMI Bar Chart not visible!"

        bars = page.locator("#emibarchart g.highcharts-series-1.highcharts-column-series:not(.highcharts-legend-item) > rect.highcharts-point")
        bars.first.wait_for(state="visible")

        bar_count = bars.count()
        print("Total Bars:", bar_count)

        assert bar_count > 0, "No bars found!"

        first_bar = bars.first
        first_bar.hover()

        tooltip = page.locator(".highcharts-tooltip")

        tooltip.wait_for(state="visible")

        tooltip_text =  tooltip.text_content()
        print("Tooltip:", tooltip_text)

        numbers = re.findall(r"[\d,.]+", tooltip_text)
        assert numbers, "No numeric data found in tooltip"

        numeric_values = [float(n.replace(",", "")) for n in numbers]
        assert all(v > 0 for v in numeric_values), \
            "Tooltip contains zero or negative values!"

        print("EMI Bar Chart validation successful")

        browser.close()
