local SLOT_COUNT = 16

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

DROPPED_ITEMS = {
    "minecraft:stone",
    "minecraft:dirt",
    "minecraft:cobblestone",
    "minecraft:sand",
    "minecraft:gravel",
    "minecraft:redstone",
    "minecraft:flint",
    "railcraft:ore_metal",
    "extrautils2:ingredients",
    "minecraft:dye",
    "thaumcraft:nugget",
    "thaumcraft:crystal_essence",
    "thermalfoundation:material",
    "projectred-core:resource_item",
    "thaumcraft:ore_cinnabar",
    "deepresonance:resonating_ore",
    "forestry:apatite"
}
function dropItems()
    print("Purging Inventory...")
    for slot = 1, SLOT_COUNT, 1 do
        local item = turtle.getItemDetail(slot)
        if(item ~= nil) then
            for filterIndex = 1, #DROPPED_ITEMS, 1 do
                if(item["name"] == DROPPED_ITEMS[filterIndex]) then
                    print("Dropping - " .. item["name"])
                    turtle.select(slot)
                    turtle.dropDown()
                end
            end
        end
    end
end

function drop_point_use()
    for slot = 1, SLOT_COUNT, 1 do
                    turtle.select(slot)
                    turtle.dropDown()
    end
end

function refuel_mid_mining()
	for slot = 1, SLOT_COUNT, 1 do
		turtle.select(slot)
		if(turtle.refuel(1)) then
			return true
		end
	end
end

function dig_and_move_forward(steps)
  for i = 1, steps do
      while turtle.detect() == true do
      	 local success, item = turtle.inspect() 
          	 if success then
              	 if item.name == "computercraft:turtle_expanded"
              	 then os.sleep(2)
  	         	 else turtle.dig()
              	 end
               end
      end
  turtle.forward()
  end
end

function dig_and_move_down(steps)
  for i = 1, steps do
      while turtle.detectDown() == true do
      	 local success, item = turtle.inspectDown() 
          	 if success then
              	 if item.name == "computercraft:turtle_expanded"
              	 then os.sleep(2)
  	         	 else turtle.digDown()
              	 end
               end
      end
  turtle.down()
  end
end


function dig_and_move_up(steps)
  for i = 1, steps do
      while turtle.detectUp() == true do
      	 local success, item = turtle.inspectUp() 
          	 if success then
              	 if item.name == "computercraft:turtle_expanded"
              	 then os.sleep(2)
  	         	 else turtle.digUp()
              	 end
               end
      end
  turtle.up()
  end
end


function calculate_steps(target_x,target_y,target_z)
  local current_x,current_y,current_z = gps.locate()

  local x_steps = current_x - target_x
  local y_steps = current_y - target_y
  local z_steps = current_z - target_z

  return x_steps,y_steps,z_steps
end

function calculate_orientation()
  local prev_x,prev_y,prev_z = gps.locate()
  dig_and_move_forward(1)
  local current_x, current_y,current_z = gps.locate()
  
  if prev_x == current_x + 1 then return 1 
  elseif prev_z == current_z + 1 then return 2 
  elseif prev_x == current_x - 1 then return 3
  elseif prev_z == current_z - 1 then return 4 
  end

end

function set_x_orientation_positive(current_orientation)
  if current_orientation == 1 then 
    return 1
  elseif current_orientation == 2 then 
    turtle.turnLeft()
	return 1
  elseif current_orientation == 3 then 
    turtle.turnLeft()
    turtle.turnLeft()
	return 1
  elseif current_orientation == 4 then
    turtle.turnRight()
	return 1
  end
 end 


function set_x_orientation_negative(current_orientation)
  if current_orientation == 1 then
    turtle.turnRight()
	turtle.turnRight()
	return 3
  elseif current_orientation == 2 then 
    turtle.turnRight()
	return 3
  elseif current_orientation == 3 then 
	return 3
  elseif current_orientation == 4 then
    turtle.turnLeft()
	return 3
  end
 end  


function set_z_orientation_positive(current_orientation)
  if current_orientation == 1 then
    turtle.turnRight()
    return 2
  elseif current_orientation == 2 then 
	return 2
  elseif current_orientation == 3 then 
    turtle.turnLeft()
	return 2
  elseif current_orientation == 4 then
    turtle.turnLeft()
    turtle.turnLeft()
	return 2
  end
 end 
 

function set_z_orientation_negative(current_orientation)
  if current_orientation == 1 then
    turtle.turnLeft()
    return 4
  elseif current_orientation == 2 then 
    turtle.turnLeft()
    turtle.turnLeft()
	return 4
  elseif current_orientation == 3 then 
    turtle.turnRight()
	return 4
  elseif current_orientation == 4 then
	return 4
  end
 end 

function navigation_to_target(x_steps, y_steps, z_steps,current_orientation)

	if x_steps >= 0 then 
	set_x_orientation_positive(current_orientation)
	current_orientation = 1 
	dig_and_move_forward(math.abs(x_steps))

	elseif x_steps < 0 then 
	set_x_orientation_negative(current_orientation)
	current_orientation = 3
	dig_and_move_forward(math.abs(x_steps))

	end

	if z_steps >= 0 then
	set_z_orientation_positive(current_orientation)
	current_orientation = 2 
	dig_and_move_forward(math.abs(z_steps))

	elseif z_steps < 0 then 
	set_z_orientation_negative(current_orientation)
	current_orientation = 4
	dig_and_move_forward(math.abs(z_steps))

	end

	if y_steps >= 0 then
	dig_and_move_down(math.abs(y_steps))

	elseif y_steps < 0 then 
	dig_and_move_up(math.abs(y_steps))

	end 
	
	return current_orientation
	
end

function return_navigation(x_steps, y_steps, z_steps,current_orientation)

	if y_steps >= 0 then
	dig_and_move_down(math.abs(y_steps))

	elseif y_steps < 0 then 
	dig_and_move_up(math.abs(y_steps))

	end 

	if z_steps >= 0 then
	set_z_orientation_positive(current_orientation)
	current_orientation = 2 
	dig_and_move_forward(math.abs(z_steps))

	elseif z_steps < 0 then 
	set_z_orientation_negative(current_orientation)
	current_orientation = 4
	dig_and_move_forward(math.abs(z_steps))

	end

	if x_steps >= 0 then 
	set_x_orientation_positive(current_orientation)
	current_orientation = 1 
	dig_and_move_forward(math.abs(x_steps))

	elseif x_steps < 0 then 
	set_x_orientation_negative(current_orientation)
	current_orientation = 3
	dig_and_move_forward(math.abs(x_steps))

	end
	
	return current_orientation
	
end

function mining_quarry(x,y,z, current_orientation)

	x_mine = x - 1

	set_x_orientation_positive(current_orientation)
	
	for i = 1, y do
	
		for q = 1, z do
		
			if z % 2 ~= 0 then
				
					if q == z then
						dig_and_move_forward(x_mine)
						turtle.turnRight()
						turtle.turnRight()
					elseif q % 2 ~= 0 then
						dig_and_move_forward(x_mine)
						turtle.turnRight()
						dig_and_move_forward(1)
						turtle.turnRight()
					else 
						dig_and_move_forward(x_mine)
						turtle.turnLeft()
						dig_and_move_forward(1)
						turtle.turnLeft()
					end
				
			else 
				
				if i % 2 ~= 0 then
	
					if q == z then
						dig_and_move_forward(x_mine)
						turtle.turnRight()
						turtle.turnRight()
					elseif q % 2 ~= 0 then
						dig_and_move_forward(x_mine)
						turtle.turnRight()
						dig_and_move_forward(1)
						turtle.turnRight()
					else 
						dig_and_move_forward(x_mine)
						turtle.turnLeft()
						dig_and_move_forward(1)
						turtle.turnLeft()
					end
						
				else
					
					if q == z then
						dig_and_move_forward(x_mine)
						turtle.turnRight()
						turtle.turnRight()
					elseif q % 2 ~= 0 then
						dig_and_move_forward(x_mine)
						turtle.turnLeft()
						dig_and_move_forward(1)
						turtle.turnLeft()
					else 
						dig_and_move_forward(x_mine)
						turtle.turnRight()
						dig_and_move_forward(1)
						turtle.turnRight()
					end
						
						
				end
				
			end
		
		end
		
	
	dropItems()
	refuel_mid_mining()
	
	if i ~= y then
	dig_and_move_down(1)
	end 
	
	end
end

function drop_point_movement(current_x, current_y, current_z)

    request_drop_point_location = "http://127.0.0.1:5000/drop_point_location?".."x="..current_x.."&y="..current_y.."&z="..current_z
	http_request = http.get(request_drop_point_location)
	drop_point_inputs = http_request.readAll()
	
	target_table = drop_point_inputs:split(",")
	
	x = tonumber(target_table[1])
	y = tonumber(target_table[2])
	z = tonumber(target_table[3])
	
	x_steps, y_steps, z_steps = calculate_steps(x,y,z)
	
	return x_steps, y_steps, z_steps
	
end
	
function docking_station_movement(current_x, current_y, current_z)

    request_docking_station_location = "http://127.0.0.1:5000/docking_station_location?".."x="..current_x.."&y="..current_y.."&z="..current_z
	http_request = http.get(request_docking_station_location)
	docking_point_inputs = http_request.readAll()
	
	target_table = docking_point_inputs:split(",")
	
	x = tonumber(target_table[1])
	y = tonumber(target_table[2])
	z = tonumber(target_table[3])
	
	x_steps, y_steps, z_steps = calculate_steps(x,y,z)
	
	return x_steps, y_steps, z_steps
	
end
	
function mining_operations()

	origin_x ,origin_y , origin_z = gps.locate()

	request_mining_location = "http://127.0.0.1:5000/mining_path"
	http_request = http.get(request_mining_location)
	mining_inputs = http_request.readAll()
	
	while mining_inputs == "no jobs" 
	do os.sleep(5)
	request_mining_location = "http://127.0.0.1:5000/mining_path"
	http_request = http.get(request_mining_location)
	mining_inputs = http_request.readAll()
	end
	 
	target_table = mining_inputs:split(",")
	 
	-- Arrays start at 1 in lua
	 
	x = tonumber(target_table[1])
	y = tonumber(target_table[2])
	z = tonumber(target_table[3])
	x_size = tonumber(target_table[4])
	y_size = tonumber(target_table[5])
	z_size = tonumber(target_table[6])

	current_orientation = calculate_orientation()
	x_steps, y_steps, z_steps = calculate_steps(x,y,z) 
	current_orientation =  navigation_to_target(x_steps, y_steps, z_steps, current_orientation)

	mining_quarry(x_size,y_size,z_size,current_orientation) 


    -- Navigation to Nearest Drop Point	
	current_orientation = calculate_orientation()
	current_x ,current_y , current_z = gps.locate()
	x_steps, y_steps, z_steps = drop_point_movement(current_x,current_y,current_z)
	return_navigation(x_steps,y_steps,z_steps, current_orientation)
	drop_point_use()
	
	-- Navigation to Docking Station	
	current_orientation = calculate_orientation()
	current_x ,current_y , current_z = gps.locate()
	x_steps, y_steps, z_steps = docking_station_movement(current_x,current_y,current_z)
	return_navigation(x_steps,y_steps,z_steps, current_orientation)


end

mining_operations()


