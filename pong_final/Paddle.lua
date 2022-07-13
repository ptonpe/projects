

Paddle = Class{}

--[[
    Note that `self` is a reference to *this* object, whichever object is
    instantiated at the time this function is called. Different objects can
    have their own x, y, width, and height values, thus serving as containers
    for data. In this sense, they're very similar to structs in C.
]]
function Paddle:init(x, y, width, height)
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.dy = 0
end

function Paddle:update(dt)
    
    if self.dy < 0 then
        self.y = math.max(0, self.y + self.dy * dt)
    else
        self.y = math.min(VIRTUAL_HEIGHT - self.height, self.y + self.dy * dt)
    end
end

function Paddle: updateAI(dt, by, bdy)
    if self.dy < 0 then
        self.y = math.max(0, by + bdy * dt)
    else 
        self.y = math.min(VIRTUAL_HEIGHT - self.height, by + bdy * dt)
    end
end


function Paddle:render()
    love.graphics.rectangle('fill', self.x, self.y, self.width, self.height)
end