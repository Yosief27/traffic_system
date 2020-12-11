sample_list = ['cat', 'dog', 'bunny', 'pig']
test = '{}'*(len(sample_list)-1)+'{}'
print(test)  # Your list of animals are: {}, {}, {}, and {}
print(test.format(*sample_list))
