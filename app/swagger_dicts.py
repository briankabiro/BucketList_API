
register_dict = {
  "parameters": [
    {
      "name": "username",
      "in": "formData",
      "description": "Username",
      "type": "string",
      "required": True
    },
    {
      "name":"password",
      "in":"formData",
      "description":"Password",
      "type": "string",
      "required":True
    }
  ],
  "responses": {
    "201": {
      "description": "Account Successfully Created"
    }
  }
}

login_dict = {
  "parameters": [
    {
      "name": "username",
      "in": "formData",
      "description": "Username of user",
      "type": "string",
      "required": True
    },
    {
      "name":"password",
      "in":"formData",
      "description": "Password of user",
      "type": "string",
      "required":True
    }
  ],
  "responses": {
    "200": {
      "description": "Username and password match"
    },
    "401":{
      "description": "The user doesn't exist"
    },
    "403": {
      "description": "The entered password is invalid"
    }
  }
}

reset_dict = {
  "parameters": [
    {
      "name": "username",
      "in": "formData",
      "type": "string",
      "required": True
    },
    {
      "name": "New Password",
      "in": "formData",
      "type": "string",
      "required": True,
      "description": "New password"     
    }
  ],
  "responses": {
    "200": {
      "description": "Password has been changed"
    },
    "404": {
      "description": "User doesn't exist"
    }
  }
}

bucketlists_get_dict = {
  "parameters":[
    {
      "name":"Authorization",
      "description":"Bearer <token>",
      "in":"header",
      "required": True,
      "type": "string",
    }
  ],
  "responses": {
    "200": {
      "description": "Bucketlists are returned"
    },
    "404":{
      "description": "The bucketlist doesn't exist"
    },
    "401": {
      "description": "Authorization header is missing"
    }
  }
}

bucketlists_post_dict = {
"parameters": [
    {
      "name": "name",
      "description":"The name of the bucketlist",
      "type": "string",
      "in": "formData",
      "required": True
    },
    {
      "name":"Authorization",
      "description":"Bearer <token>",
      "in":"header",
      "required": True,
      "type": "string"
    }
  ],
  "responses": {
    "201": {
      "description": "Bucketlist is created"
    },
    "401": {
      "description": "Authorization header is missing"
    }
  }  
}


bucketlist_get_dict = {
  "parameters": [
    {
      "name": "id",
      "description":"Id of the bucketlist",
      "in": "path",
      "type": "integer",
      "required": True
    },
    {
      "name":"Authorization",
      "description":"Bearer <token>",
      "in":"header",
      "required": True,
      "type": "string",
    }
  ],
  "responses": {
    "200": {
      "description": "Bucketlist with specified id is returned"
    },
    "401": {
      "description": "Authorization header is missing"
    }
  }  
}
bucketlist_put_dict = {
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "type": "integer",
      "description":"Id of the bucketlist",
      "required": True
    },
    {
      "name": "name",
      "in": "formData",
      "type":"string",
      "required": True,
      "description":"Name of the bucketlist"
    },
    {
      "name":"Authorization",
      "description":"Bearer <token>",
      "in":"header",
      "required": True,
      "type": "string",

    }
  ],
  "responses": {
    "200": {
      "description": "Name of bucketlist with specified id is updated"
    },
    "401": {
      "description": "Authorization header is missing"
    }
  }  
}

bucketlist_delete_dict = {
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "type": "integer",
      "required": True,
      "description":"Id of the bucketlist"
    },
    {
      "name":"Authorization",
      "description":"Bearer <token>",
      "in":"header",
      "required": True,
      "type": "string"
    }
  ],
  "responses": {
    "200": {
      "description": "Bucketlist with specified id is deleted"
    },
    "401": {
      "description": "Authorization header is missing"
    }
  }  
}

items_get_dict = {
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "type":"string",
      "required": True,
      "description":"Id of the bucketlist"
    },
    {
      "name": "query",
      "in": "query",
      "type": "string"
    },
    {
      "name": "limit",
      "in":"query",
      "type":"string"
    },
    {
      "name":"Authorization",
      "description":"Bearer <token>",
      "in":"header",
      "required": True,
      "type": "string",

    }
  ],
  "responses": {
    "200": {
      "description": "Get items in bucketlist"
    },
    "400":{
      "description": "Bad request. Limit or query isn't defined"
    },
    "401": {
      "description": "Authorization header is missing"
    }
  }  
}

items_post_dict = {
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "type": "integer",
      "required": True,
      "description":"Id of the bucketlist"
    },
    {
      "name": "description",
      "in": "formData",
      "description":"Title of the item",
      "type":"string",
      "required": True
    },
    {
      "name":"Authorization",
      "description":"Bearer <token>",
      "in":"header",
      "required": True,
      "type": "string",

    }
  ],
  "responses": {
    "201": {
      "description": "Create a new item"
    },
    "401": {
      "description": "Authorization header is missing"
    }
  }  
}

item_put_dict = {
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "type": "integer",
      "required": True
    },
    {
      "name": "item_id",
      "in": "path",
      "type":"string",
      "required": True
    },
    {
      "name": "description",
      "in": "formData",
      "type":"string",
      "required": True,
      "description":"Title of the Item"
    },
    {
      "name":"Authorization",
      "description":"Bearer <token>",
      "in":"header",
      "required": True,
      "type": "string",

    }
  ],
  "responses": {
    "200": {
      "description": "Item title is updated"
    },
    "401": {
      "description": "Authorization header is missing"
    }
  }  
}

item_delete_dict = {
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "type": "integer",
      "required": True
    },{
      "name":"item_id",
      "in":"path",
      "type":"integer",
      "required": True
    },
    {
      "name":"Authorization",
      "description":"Bearer <token>",
      "in":"header",
      "required": True,
      "type": "string"
    }
  ],
  "responses": {
    "200": {
      "description": "Item is deleted from bucketlist"
    },
    "401": {
      "description": "Authorization header is missing"
    }
  }   
}