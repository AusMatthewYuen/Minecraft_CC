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

function reshuffle_turtle()
   	local success, item = turtle.inspectDown() 
   	if success then
       	if item.name == "computercraft:turtle_expanded" then
         turtle.digUp()
         turtle.dropDown()
         end
     end
end

function mining_deployment()

    mining_turtle_deploy = turtle.suckDown(1)
    
    print(mining_turtle_deploy)
    
    if mining_turtle_deploy == true
    
        then
    
        turtle.place()
        newTurtle = peripheral.wrap("front")
        newTurtle.turnOn()
        os.sleep(4)
    
        while(turtle.detect()) do
        	os.sleep(0.5)
        	reshuffle_turtle()
        end
    
    else
        os.sleep(2)
        print("no turtles available")
    end
    
end
	

while true do 

	mining_jobs_available = "http://127.0.0.1:5000/mining_jobs_available"
	http_request = http.get(mining_jobs_available)
	mining_inputs = http_request.readAll()
	
	if mining_inputs == 0 then
    	print("no jobs available")
    	os.sleep(2)
        reshuffle_turtle()
    	
    else mining_deployment()
    
    end
    
    reshuffle_turtle()
        
	
end