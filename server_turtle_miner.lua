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

function mining_deployment()

    turtle.suckDown(1)
    turtle.place()
    newTurtle = peripheral.wrap("front")
    newTurtle.turnOn()
    os.sleep(2)

    while(turtle.detect()) do
    	os.sleep(0.5)
    end
    

    	end
    end    
end
	
turtle.turnLeft()


while true do 

	mining_jobs_available = "http://127.0.0.1:5000/mining_jobs_available"
	http_request = http.get(mining_jobs_available)
	mining_inputs = http_request.readAll()
	
	if mining_inputs == 0 then
    	os.sleep(2)
    	
    else mining_deployment()
        
	
end