#!/usr/bin/env python

import pandas as pd
import numpy as np

DEV_PROCEEDS = 9.99 * 0.7

# importing data
df = pd.read_csv("data_analytics.csv")
df['Event Date'] = df['Event Date'].astype('datetime64')

# easy way of calculating LTV applicable for our data
alt_ltv = DEV_PROCEEDS*sum(df['Subscription Offer Type'].isna())/sum(df['Subscription Offer Type'].notna())
print("Alternative method of computing the LTV:\nLTV = ", alt_ltv)

# now lets compare it with the formula given in competition's task

# grouping data by users: finding out amount of their subscribtions and registration dates
grouped = df.groupby('Subscriber ID')
aggregated = grouped.agg({'Event Date' : ['count', 'min']})['Event Date'].rename(columns={"min": "registration", "count": "subscriptions"})

#As all users in dataset have complete lifetimes, can count conversions using all records on each step

#counting how much users having specific amount of subscriptions
funnel = aggregated.groupby('subscriptions').count().reset_index()
funnel = funnel.sort_values('subscriptions', ascending = False)

#counting the funnel: what amount of users having at least specific amount of sbscriptions
funnel['registration'] = np.cumsum(funnel['registration'])
funnel = funnel.sort_values('subscriptions')

# calculating convertion rates
fun_amounts = funnel['registration']
fun_percents = [1.] + list(np.array(fun_amounts[1:] )/np.array(fun_amounts[:-1]))
funnel['convertion'] = fun_percents

convs = np.array(funnel['convertion'] [1:])

#calculating LTV using the formula given in task
vals = [DEV_PROCEEDS]
for i in range(len(convs)):
    vals.append(vals[-1]*convs[i])

ltv = sum(vals[1:])
ltv
print("Proposed method of computing the LTV:\nLTV = ", ltv)