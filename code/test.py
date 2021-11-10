s = 'fgfdg/fdgfdg/dfgdfgdfg/авп'

end_f = s.rfind('/')

# print(s.rfind('/'))

print(s[:end_f+1]+'(f)'+s[end_f+1:])