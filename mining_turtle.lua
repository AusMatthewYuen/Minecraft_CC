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

function dig_and_move_forward(steps)
  for i = 1, steps do
  while turtle.detect() == true do
	 turtle.dig()
     end
  turtle.forward()
  end
end

function dig_and_move_down(steps)
  for i = 1, steps do
  while turtle.detectDown() == true do
	 turtle.digDown()
     end
  turtle.down()
  end
end

function dig_and_move_up(steps)
  for i = 1, steps do
  while turtle.detectUp() == true do
	 turtle.digUp()
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
	local current_orientation = 1 
	dig_and_move_forward(math.abs(x_steps))

	elseif x_steps < 0 then 
	set_x_orientation_negative(current_orientation)
	local current_orientation = 3
	dig_and_move_forward(math.abs(x_steps))

	end

	if z_steps >= 0 then
	set_z_orientation_positive(current_orientation)
	local current_orientation = 2 
	dig_and_move_forward(math.abs(z_steps))

	elseif z_steps < 0 then 
	set_z_orientation_negative(current_orientation)
	local current_orientation = 4
	dig_and_move_forward(math.abs(z_steps))

	end

	if y_steps >= 0 then
	dig_and_move_down(math.abs(y_steps))

	elseif y_steps < 0 then 
	dig_and_move_up(math.abs(y_steps))

	end 
	
	return current_orientation
	
end

function mining_quarry(x,y,z, current_orientation)

	x_mine = x - 1

	if current_orientation == 2 then
		turtle.turnLeft()
	elseif current_orientation == 4 then
		turtle.turnRight()
	end
	
	for i = 1, y do
	
		if (i % 2) ~= 0 then
			for q = 1, z do
				if q == 1 and i == 1 then
				dig_and_move_forward(x_mine)
				turtle.turnLeft()
				dig_and_move_forward(1)
				turtle.turnLeft()
				elseif q == z then
				turtle.turnLeft()
				turtle.turnLeft()
				dig_and_move_forward(x_mine)
				elseif (q % 2) == 0 then
				dig_and_move_forward(x_mine)
				turtle.turnLeft()
				dig_and_move_forward(1)
				turtle.turnLeft()
				elseif (q % 2) ~= 0 then
				dig_and_move_forward(x_mine)
				turtle.turnRight()
				dig_and_move_forward(1)
				turtle.turnRight()
				end
			end
					
		else
			for q = 1, z do
				if q == 1 then 
				turtle.turnLeft()
				turtle.turnLeft()
				turtle.dig_and_move_forward(x_mine)
				elseif q == z then
				dig_and_move_forward(x_mine)
				elseif (q % 2) == 0 then
				dig_and_move_forward(x_mine)
				turtle.turnRight()
				dig_and_move_forward(1)
				turtle.turnRight()
				elseif (q % 2) ~= 0 then
				dig_and_move_forward(x_mine)
				turtle.turnLeft()
				dig_and_move_forward(1)
				turtle.turnLeft()
				end
			end
		
		end
	dig_and_move_down(1)	
	end
end
	
	
	


current_orientation = calculate_orientation()
x_steps, y_steps, z_steps = calculate_steps(11,66,144)
current_orientation2 =  navigation_to_target(x_steps, y_steps, z_steps, current_orientation)

mining_quarry(5,5,5,current_orientation2)



