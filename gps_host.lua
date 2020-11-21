function string:split(delimiter)
  local result = { }
  local from  = 1
  local delim_from, delim_to = string.find( self, delimiter, from  )
  while delim_from do
    table.insert( result, string.sub( self, from , delim_from-1 ) )
    from  = delim_to + 1
    delim_from, delim_to = string.find( self, delimiter, from  )
  end
  table.insert( result, string.sub( self, from  ) )
  return result
end
 
computer_id = os.getComputerID()
computer_label = os.getComputerLabel()
 
computer_request_location = "http://127.0.0.1:5000/GPS_Setup?computer_id="..computer_id
http_request = http.get(computer_request_location)
computer_location = http_request.readAll()
 
location_table = computer_location:split(",")
 
-- Arrays start at 1
 
x = location_table[1]
y = location_table[2]
z = location_table[3]
 
shell.run("gps","host",x,y,z)
 
print(computer_location)