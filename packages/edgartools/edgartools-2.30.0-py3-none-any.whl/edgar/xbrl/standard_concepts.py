from edgar import Company
from edgar.reference.tickers import get_companies_by_exchange

from typing import List, Dict
import pandas as pd
from tqdm.auto import tqdm
from pydantic import BaseModel


class StandardConcept(BaseModel):
    concept: str
    label: str
    order: int

class StandardStatement(BaseModel):
    name: str
    concepts: List[StandardConcept]

def get_financials(ticker):
    company = Company(ticker, include_old_filings=False)
    if company:
        financials = company.financials
        if financials:
            return (get_statement_dataframe(ticker, financials.get_balance_sheet()), 
                    get_statement_dataframe(ticker, financials.get_income_statement()), 
                    get_statement_dataframe(ticker, financials.get_cash_flow_statement()),
                    get_statement_dataframe(ticker, financials.get_statement_of_changes_in_equity()),
                    get_statement_dataframe(ticker, financials.get_statement_of_comprehensive_income()))

def get_statement_dataframe(ticker, statement):
    df = (statement.get_dataframe(include_concept=True, include_format=True)
          .reset_index().filter(['label', 'primary_concept', 'decimals']))
    df['Ticker'] = ticker
    return df

def learn_standard_concepts_from_companies(tickers:List[str]) -> Dict[str, StandardStatement]:
    """
    Load the balance sheet, income statement and cash flow statements for the sample
    of companies then learn which concepts are commonly used and therefore standard
    """
    
    balance_sheets = []
    cashflows = []
    incomes = []
    equities = []
    comprehensive_incomes = []
    for ticker in tqdm(tickers):
        financials = get_financials(ticker)
        if financials:
            balance_sheet, income, cashflow, equity, comprehensive_income = financials
            balance_sheets.append(balance_sheet)
            incomes.append(income)
            cashflows.append(cashflow)
            equities.append(equity)
            comprehensive_incomes.append(comprehensive_income)

    balance_sheet_data = pd.concat(balance_sheets)
    income_statement_data = pd.concat(incomes)
    cashflow_data = pd.concat(cashflows)
    equity_data =  pd.concat(equities)
    comprehensive_income_data = pd.concat(comprehensive_incomes)

    def analyze_common_concepts(df, statement_type):
        #concept_counts = df['primary_concept'].value_counts()
        #label_counts = df['label'].value_counts()
        
        # Calculate the percentage of companies using each primary_concept
        company_count = df['Ticker'].nunique()
        concept_company_counts = df.groupby('primary_concept')['Ticker'].nunique()
        concept_percentages = (concept_company_counts / company_count * 100).sort_values(ascending=False)
        
        # Get the most common label for each primary_concept
        concept_labels = df.groupby('primary_concept')['label'].agg(lambda x: x.value_counts().index[0])
        
        # Get the average order of each primary_concept
        df['order'] = df.groupby('Ticker').cumcount()
        concept_orders = df.groupby('primary_concept')['order'].mean().sort_values()
        
        return concept_percentages, concept_labels, concept_orders

    standard_statements = {}
    generated_code = []

    for statement_type, df in [
        ("Balance Sheet", balance_sheet_data),
        ("Income Statement", income_statement_data),
        ("Cash Flow Statement", cashflow_data),
        ("Statement of Changes in Equity", equity_data),
        ("Statement of Comprehensive Income", comprehensive_income_data)
    ]:
        concept_percentages, concept_labels, concept_orders = analyze_common_concepts(df, statement_type)
        
        # Filter concepts used by more than 80% of companies
        threshold = 70
        standard_concepts = [
            StandardConcept(
                concept=concept,
                label=concept_labels[concept],
                order=int(concept_orders[concept])
            )
            for concept, percentage in concept_percentages.items()
            if percentage > threshold
        ]
        
        # Sort standard concepts by their order
        standard_concepts.sort(key=lambda x: x.order)
        
        standard_statement = StandardStatement(
            name=statement_type,
            concepts=standard_concepts
        )
        standard_statements[statement_type] = standard_statement

        # Generate code for this statement
        variable_name = statement_type.lower().replace(" ", "_")
        code = f"{variable_name} = StandardStatement(\n"
        code += f"    name=\"{statement_type}\",\n"
        code += "    concepts=[\n"
        for concept in standard_concepts:
            code += f"        StandardConcept(primary_concept=\"{concept.concept}\", label=\"{concept.label}\", order={concept.order}),\n"
        code += "    ]\n"
        code += ")\n"
        generated_code.append(code)

    # Print the generated code
    print("# Generated code for standard statements:")
    print("\n".join(generated_code))

    return standard_statements

def analyze_statement_concepts(statement_data: pd.DataFrame, standard_statement: StandardStatement) -> Dict[str, float]:
    """
    Analyze the concepts used in a statement compared to standard concepts.
    
    Args:
        statement_data (pd.DataFrame): The financial statement data to analyze.
        standard_statement (StandardStatement): The standard statement to compare against.
    
    Returns:
        Dict[str, float]: Dictionary of primary_concept usage percentages and order similarity.
    """
    if statement_data is None or standard_statement is None:
        return {
            "standard_concepts_used": 0,
            "statement_concepts_standard": 0,
            "order_similarity": 0,
        }

    statement_concepts = set(statement_data['primary_concept'].unique())
    standard_concepts = set(concept.concept for concept in standard_statement.concepts)
    
    total_concepts = len(statement_concepts)
    standard_used = statement_concepts.intersection(standard_concepts)
    
    # Calculate order similarity
    statement_order = {concept: i for i, concept in enumerate(statement_data['primary_concept'])}
    standard_order = {concept.concept: i for i, concept in enumerate(standard_statement.concepts)}
    
    common_concepts = set(statement_order.keys()) & set(standard_order.keys())
    if common_concepts:
        order_diff = sum(abs(statement_order[c] - standard_order[c]) for c in common_concepts)
        max_diff = len(common_concepts) ** 2
        order_similarity = 1 - (order_diff / max_diff)
    else:
        order_similarity = 0
    
    return {
        "standard_concepts_used": len(standard_used) / len(standard_concepts) if standard_concepts else 0,
        "statement_concepts_standard": len(standard_used) / total_concepts if total_concepts > 0 else 0,
        "order_similarity": order_similarity,
    }

if __name__ == '__main__':
    samples = 50
    tickers = get_companies_by_exchange("NASDAQ").head(samples).ticker.tolist()
    standard_statements = learn_standard_concepts_from_companies(tickers=tickers)
    
    print("Standard Statements:")
    for statement_type, standard_statement in standard_statements.items():
        print(f"\n{statement_type}:")
        for concept in standard_statement.concepts:
            print(f"  {concept.order}. {concept.concept}: {concept.label}")

    # You can add more example usage or testing code here