from re import findall

str = "aasdf(sfsdsd)!fsfsdfsdf-sd"
reg_kernel = '[а-яёa-z-()]+'


result = findall(reg_kernel, str)

print(''.join(result))