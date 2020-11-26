slots = 16

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

turtle.suckDown(1)
turtle.place()
panda = turtle.inspect()
print(panda)
newTurtle = peripheral.wrap("front")
newTurtle.turnOn()
os.sleep(15)
turtle.dig()
turtle.turnRight()

for i = 1, slots do 
	turtle.getSelectedSlot(i)
	print(i)
	print(turtle.getItemDetail(i))
end
	
turtle.turnLeft()