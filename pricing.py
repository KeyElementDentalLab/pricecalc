from flask import Flask, request, render_template_string

app = Flask(__name__)

# ---------- Product Data for Pricing Analysis ----------
PRODUCTS = {
    "Master Tier - Feldspathic Veneer": 450,
    "Master Tier - Master Lithium Disilicate": 390,
    "Master Tier - Master Zirconia Crown/Pontic": 390,
    "Master Tier - Layered Zirconia": 390,
    "Master Tier - Cantilever Bridge": 390,
    "Master Tier - Zirconia Maryland Bridge": 390,
    "Master Tier - Veneer": 390,
    "Master Tier - Lithium Disilicate Implant Crown (Screw-Retained)": 799,
    "Master Tier - Zirconia Implant Crown (Screw-Retained)": 799,
    "Master Tier - Lithium Disilicate Implant Crown (Cementable)": 759,
    "Master Tier - Zirconia Implant Crown (Cementable)": 759,
    "Premium Tier - Premium Lithium Disilicate (Anterior)": 298,
    "Premium Tier - Premium Lithium Disilicate (Posterior)": 210,
    "Premium Tier - Premium Zirconia Crown/Pontic (Anterior)": 298,
    "Premium Tier - Premium Zirconia Crown/Pontic (Posterior)": 198,
    "Premium Tier - Layered Zirconia (Anterior)": 298,
    "Premium Tier - Layered Zirconia (Posterior)": 250,
    "Premium Tier - Cantilever Bridge (Anterior)": 298,
    "Premium Tier - Cantilever Bridge (Posterior)": 198,
    "Premium Tier - Zirconia Maryland Bridge": 298,
    "Premium Tier - Veneer": 298,
    "Premium Tier - Lithium Disilicate Implant (Anterior)": 707,
    "Premium Tier - Lithium Disilicate Implant (Posterior)": 680,
    "Premium Tier - Zirconia Crown Implant (Anterior)": 707,
    "Premium Tier - Zirconia Crown Implant (Posterior)": 560,
    "Premium Tier - PMMA SR Implant Crown": 194,
    "Premium Tier - Model-Less Implant Crown (Posterior)": 460,
    "Premium Tier - Lithium Disilicate Implant (Cementable, Anterior)": 707,
    "Premium Tier - Lithium Disilicate Implant (Cementable, Posterior)": 640,
    "Premium Tier - Zirconia Crown Implant (Cementable, Anterior)": 707,
    "Premium Tier - Zirconia Crown Implant (Cementable, Posterior)": 520,
    "Premium Tier - Model-Less Implant Crown (Post, Cementable)": 460,
    "Hybrid Restorations - Hybrid FP1 Monolithic": 6900,
    "Hybrid Restorations - Hybrid FP3": 4999,
    "Hybrid Restorations - Hybrid Printed Prototype": 250,
    "Hybrid Restorations - Screw Retained Hybrid PMMA": 1500,
    "Hybrid Restorations - FP2 Pink Porcelain Per Tooth": 80,
    "Additional Services - ASC Implant Driver": 80,
    "Additional Services - Seating Jig": 35,
    "Additional Services - Verification Jig Per Cylinder": 65,
    "Additional Services - Digital Implant Model/Tissue": 38,
    "Additional Services - Lab Analog": 50,  # approximate average
    "Digital Diagnostic Design - Per Tooth": 58,
    "Digital Diagnostic Design - Clear Injection Matrix": 60,
    "Digital Diagnostic Design - Gingivectomy Guide": 170,
    "Digital Diagnostic Design - Injection Every Other Tooth Model": 50,
    "Digital Diagnostic Design - Reduction Guide Suck-Down": 110,
    "Digital Diagnostic Design - Reduction Matrix": 30,
    "Digital Diagnostic Design - Provisional/Temp Crown": 67,
    "Digital Diagnostic Design - Diagnostic Design/Temp Combo": 105,
    "Digital Diagnostic Design - PMMA Palatal Jig": 60,
    "Other Services - Custom Shade": 50,
    "Other Services - Final Screw": 30,
    "Other Services - Semi-Adjustable Articulation": 35,
    "Other Services - Print Model": 35,
    "Other Services - Reduction Coping": 25,
    "Other Services - Seating Jig": 35
}

# ---------- Explanation Text for General Labor Cost Calculation (Tab 2) ----------
LABOR_EXPLANATION = """\
When calculating general labor cost, you generally want to determine how much you’re paying your employees per hour and then factor in the number of hours worked. Here’s a step‐by‐step approach:

1. Determine the Hourly Wage or Salary Conversion:
   - Hourly Employees: Use their hourly wage directly.
   - Salaried Employees: Convert their annual salary to an hourly rate.
     For example, if an employee earns $52,000 a year and works 2,080 hours per year 
     (which is 40 hours/week × 52 weeks), the hourly rate is:
     
         Hourly Rate = $52,000 / 2,080 ≈ $25 per hour

2. Include Additional Labor Costs:
   - Benefits & Payroll Taxes: Often, you need to add on a percentage for benefits 
     (health insurance, retirement, etc.) and payroll taxes.
     
     For example, if benefits add 20% on top of the base wage:
     
         Effective Hourly Cost = Base Hourly Wage × (1 + 0.20)
     
     So, for a $25 per hour employee:
     
         $25 × 1.20 = $30 per hour

3. Calculate Total Labor Cost for a Given Period:
   - Multiply the effective hourly cost by the total number of hours worked in the period.
     
     For instance, if an employee works 160 hours in a month:
     
         Monthly Labor Cost = $30 × 160 = $4,800

4. Determine Labor Cost Per Unit (if applicable):
   - If you’re producing items, divide the total labor cost for the period by the 
     number of units produced.
     
     For example, if 500 units are produced in that month:
     
         Labor Cost per Unit = $4,800 / 500 = $9.60 per unit

5. Adjust for Multiple Employees or Shifts:
   - If you have several employees or multiple shifts, calculate each employee’s effective 
     cost and add them together to get your total labor cost for the period.
"""

# ---------- Explanation Text for Overhead Time Period Considerations (Tab 3) ----------
OVERHEAD_EXPLANATION = """\
Considerations When Choosing a Time Period for Overhead Allocation

Production Cycle:
   - High-Volume, Continuous Production:
       If you produce units daily and your overhead costs are relatively stable from day-to-day,
       a daily or weekly overhead allocation might provide a more precise picture of per-unit overhead.
   - Batch Production:
       If production occurs in batches or if you have a lower volume, calculating overhead on a per-batch basis might be more useful.

Stability of Overhead Costs:
   - Overhead costs like rent or salaried administrative expenses typically don't fluctuate dramatically day-to-day.
     If these costs are relatively fixed, a monthly calculation might be acceptable.
   - However, if your overhead has significant daily or weekly variations (perhaps due to variable utility usage or other operational costs),
     using a shorter period could yield a more accurate per-unit cost.

Purpose of the Analysis:
   - Pricing and Profitability:
       For setting prices and understanding profitability per unit, you want a period that matches how frequently you sell or produce units.
       If you sell a high volume every day, breaking it down on a daily basis might give you clearer insight.
   - Financial Planning:
       For broader financial planning, a monthly or quarterly analysis is often more common.

Example Approaches:
   - Daily Approach:
         If your overhead costs total $500 per day and you produce 100 units per day,
         Overhead per Unit = $500 / 100 = $5 per unit.
   - Weekly Approach:
         If your overhead costs total $3,500 per week and you produce 700 units per week,
         Overhead per Unit = $3,500 / 700 = $5 per unit.
   - Monthly Approach:
         If monthly overhead is $8,350 and you produce 1,000 units per month,
         Overhead per Unit = $8,350 / 1,000 = $8.35 per unit.

Final Recommendation:
   Choose the time period that best reflects your actual production and cost patterns.
   If your production is very dynamic and you want a more precise per-unit analysis, consider a daily or weekly measure.
   If production is steady or the overhead costs are better tracked monthly, then monthly is acceptable.
   The key is consistency and ensuring that the chosen time frame truly represents how your costs and production levels behave.

By aligning your overhead allocation period with your production cycle, you’ll get a more accurate per-unit cost analysis that can better inform your pricing and business decisions.
"""

# ---------- HTML Templates as Multi-line Strings ----------

PRICING_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Pricing Analysis</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    .container { max-width: 800px; margin: auto; }
    .error { color: red; }
    label { display: block; margin-top: 10px; }
    input, select { padding: 5px; width: 100%; max-width: 400px; }
    .result { background-color: #f0f0f0; padding: 10px; margin-top: 20px; border-radius: 5px; }
    nav a { margin-right: 15px; }
  </style>
</head>
<body>
  <div class="container">
    <nav>
      <a href="/">Pricing Analysis</a>
      <a href="/labor">Labor Cost Explanation</a>
      <a href="/overhead">Overhead Considerations</a>
    </nav>
    <h1>Pricing Analysis</h1>
    {% if error %}
      <p class="error">{{ error }}</p>
    {% endif %}
    <form method="post">
      <label for="product">Select Product:</label>
      <select name="product" id="product">
        {% for prod in products.keys() %}
          <option value="{{ prod }}"
          {% if selected_product == prod %} selected {% endif %}>
            {{ prod }}
          </option>
        {% endfor %}
      </select>

      <label for="unit_price">Unit Price ($):</label>
      <input type="number" step="any" name="unit_price" id="unit_price"
             value="{% if result %}{{ result.unit_price | replace('$','') }}{% else %}{{ (products|dictsort(true))[0][1] }}{% endif %}">

      <label for="material_cost">Material Cost ($):</label>
      <input type="number" step="any" name="material_cost" id="material_cost" value="0">

      <label for="labor_cost">Labor Cost ($):</label>
      <input type="number" step="any" name="labor_cost" id="labor_cost" value="0">

      <label for="qc_cost">Quality Control Cost ($):</label>
      <input type="number" step="any" name="qc_cost" id="qc_cost" value="0">

      <label for="overhead_cost">Overhead Cost ($):</label>
      <input type="number" step="any" name="overhead_cost" id="overhead_cost" value="0">

      <br>
      <button type="submit" style="margin-top:15px;">Calculate Break-Even &amp; Margin</button>
    </form>

    {% if result %}
      <div class="result">
        <h2>Break-Even Analysis</h2>
        <p><strong>Product:</strong> {{ result.product }}</p>
        <p><strong>Unit Price:</strong> {{ result.unit_price }}</p>
        <p><strong>Total Variable Cost:</strong> {{ result.total_variable_cost }}</p>
        <p><strong>Contribution Margin per Unit:</strong> {{ result.contribution_margin }}</p>
        <p><strong>Break-Even Quantity:</strong> {{ result.break_even_qty }}</p>
        <p><strong>Profit Margin:</strong> {{ result.profit_margin }}</p>
        <h3>Cost Driver Breakdown</h3>
        <p><strong>Material:</strong> {{ result.material_pct }}</p>
        <p><strong>Labor:</strong> {{ result.labor_pct }}</p>
        <p><strong>Quality Control:</strong> {{ result.qc_pct }}</p>
      </div>
    {% endif %}
  </div>
  
  <!-- JavaScript to update unit price on product change -->
  <script>
    const products = {{ products | tojson }};
    const productSelect = document.getElementById("product");
    const unitPriceInput = document.getElementById("unit_price");
    productSelect.addEventListener("change", function() {
      const selectedProduct = productSelect.value;
      unitPriceInput.value = products[selectedProduct];
    });
  </script>
</body>
</html>
"""

LABOR_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Labor Cost Explanation</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
    .container { max-width: 800px; margin: auto; }
    nav a { margin-right: 15px; }
    pre { background-color: #f0f0f0; padding: 15px; border-radius: 5px; }
  </style>
</head>
<body>
  <div class="container">
    <nav>
      <a href="/">Pricing Analysis</a>
      <a href="/labor">Labor Cost Explanation</a>
      <a href="/overhead">Overhead Considerations</a>
    </nav>
    <h1>Labor Cost Explanation</h1>
    <pre>{{ explanation }}</pre>
  </div>
</body>
</html>
"""

OVERHEAD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Overhead Time Period Considerations</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
    .container { max-width: 800px; margin: auto; }
    nav a { margin-right: 15px; }
    pre { background-color: #f0f0f0; padding: 15px; border-radius: 5px; }
  </style>
</head>
<body>
  <div class="container">
    <nav>
      <a href="/">Pricing Analysis</a>
      <a href="/labor">Labor Cost Explanation</a>
      <a href="/overhead">Overhead Considerations</a>
    </nav>
    <h1>Overhead Time Period Considerations</h1>
    <pre>{{ explanation }}</pre>
  </div>
</body>
</html>
"""

# ---------- Routes ----------

@app.route('/', methods=["GET", "POST"])
def pricing_analysis():
    error = None
    result = None
    selected_product = None
    if request.method == "POST":
        selected_product = request.form.get("product")
        unit_price = request.form.get("unit_price")
        material_cost = request.form.get("material_cost")
        labor_cost = request.form.get("labor_cost")
        qc_cost = request.form.get("qc_cost")
        overhead_cost = request.form.get("overhead_cost")
        try:
            unit_price = float(unit_price)
            material_cost = float(material_cost)
            labor_cost = float(labor_cost)
            qc_cost = float(qc_cost)
            overhead_cost = float(overhead_cost)
        except ValueError:
            error = "Please enter valid numeric values for all cost fields."
        else:
            total_variable_cost = material_cost + labor_cost + qc_cost
            contribution_margin = unit_price - total_variable_cost
            if contribution_margin <= 0:
                break_even_qty = "Not achievable (costs exceed or equal price)"
            else:
                break_even_qty = overhead_cost / contribution_margin
            profit_margin = (contribution_margin / unit_price) * 100 if unit_price > 0 else 0
            if total_variable_cost > 0:
                material_pct = (material_cost / total_variable_cost) * 100
                labor_pct = (labor_cost / total_variable_cost) * 100
                qc_pct = (qc_cost / total_variable_cost) * 100
            else:
                material_pct = labor_pct = qc_pct = 0

            result = {
                "product": selected_product,
                "unit_price": f"${unit_price:.2f}",
                "total_variable_cost": f"${total_variable_cost:.2f}",
                "contribution_margin": f"${contribution_margin:.2f}",
                "break_even_qty": break_even_qty if isinstance(break_even_qty, str) else f"{break_even_qty:.2f} units",
                "profit_margin": f"{profit_margin:.2f}%",
                "material_pct": f"{material_pct:.2f}%",
                "labor_pct": f"{labor_pct:.2f}%",
                "qc_pct": f"{qc_pct:.2f}%"
            }
    return render_template_string(PRICING_TEMPLATE, products=PRODUCTS, error=error, result=result, selected_product=selected_product)

@app.route("/labor")
def labor_explanation():
    return render_template_string(LABOR_TEMPLATE, explanation=LABOR_EXPLANATION)

@app.route("/overhead")
def overhead_explanation():
    return render_template_string(OVERHEAD_TEMPLATE, explanation=OVERHEAD_EXPLANATION)

if __name__ == "__main__":
    app.run(debug=True)