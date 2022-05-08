import os
import matplotlib.pyplot as plt
import numpy as np


def autoPct(values):
    def customPct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.0f}%  (${v:d})'.format(p=pct, v=val)
    return customPct


def createExpenseReport(jsonObj):
    filepath = os.path.abspath(os.getcwd())
    expenseCatNames = []
    tempDict = {}

    # search for the "Expenses" account
    for account in jsonObj["accounts"]:
        if account["name"] == "Expenses":

            # once the "Expenses" account is found, check if there are any transactions not tied to subaccounts
            if account["transactions"]:
                # if so, add them to the temp dict and create a Miscellaneous expense category in expenseCatNames list
                tempDict.update({account["id"]: account["transactions"]})
                expenseCatNames.append("Miscellaneous")

            # go through each subaccount listed in the Expenses subaccount array
            for subAccount in account["subaccounts"]:
                # add each subaccount and its related transactions to the temp dict
                tempDict.update({jsonObj["accounts"][int(subAccount) - 1]["id"]: jsonObj["accounts"][int(subAccount) - 1]["transactions"]})
                # add the expense category name to expenseCatNames list
                expenseCatNames.append(jsonObj["accounts"][int(subAccount) - 1]["name"])
            break

    # prepare category names and expense amounts for the pie chart
    expenseCatNums = tempDict.keys()
    expenseAmounts = []
    for category in expenseCatNums:
        # sum the totals of each transaction in the expense category
        amount = 0
        for transaction in tempDict[category]:
            # check if the amount should be a debit or credit
            if jsonObj["transactions"][int(transaction) - 1]["debit"] == category:
                amount += int(jsonObj["transactions"][int(transaction) - 1]["amount"])
            else:
                amount += -int(jsonObj["transactions"][int(transaction) - 1]["amount"])
        expenseAmounts.append(amount)

    if not expenseAmounts:
        return "No expenses to report"

    # create and save the pie chart
    expenseAmounts = np.array(expenseAmounts)
    plt.pie(expenseAmounts, labels=expenseCatNames, autopct=autoPct(expenseAmounts))
    plt.title("Expense Summary")
    filename = "expense_report.pdf"
    plt.savefig(filename)

    return filepath + "\\" + filename

