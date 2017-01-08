import pandas

top_companies = pandas.read_table("../data/top_companies.txt", sep='\t')
print list(top_companies)
print top_companies.shape
