
register_dict = {
  "parameters": [
    {
      "name": "username",
      "in": "formData",
      "type": "string",
      "required": True
    },
    {
      "name":"password",
      "in":"formData",
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
      "type": "string",
      "required": True
    },
    {
      "name":"password",
      "in":"formData",
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
    }
  ],
  "responses": {
    "200": {
      "description": "Password has been changed"
    }
  }
}

bucketlists_get_dict = {
  "responses": {
    "200": {
      "description": "Bucketlists are returned"
    },
    "404":{
      "description": "The bucketlist doesn't exist"
    },
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
      "in":"headers",
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
      "in": "path",
      "type": "integer",
      "required": True
    }
  ],
  "responses": {
    "200": {
      "description": "Bucketlist with specified id is returned"
    }
  }  
}
bucketlist_put_dict = {
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "type": "integer",
      "required": True
    },
    {
      "name": "name",
      "in": "formData",
      "type":"string",
      "required": True
    }
  ],
  "responses": {
    "200": {
      "description": "Name of bucketlist with specified id is updated"
    }
  }  
}

bucketlist_delete_dict = {
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "type": "integer",
      "required": True
    }
  ],
  "responses": {
    "200": {
      "description": "Bucketlist with specified id is deleted"
    }
  }  
}

items_get_dict = {
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "type":"string",
      "required": True
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
    }
  ],
  "responses": {
    "200": {
      "description": "Get items in bucketlist"
    }
  }  
}

items_post_dict = {
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "type": "integer",
      "required": True
    },
    {
      "name": "description",
      "in": "formData",
      "type":"string",
      "required": True
    }
  ],
  "responses": {
    "201": {
      "description": "Create a new item"
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
      "required": True
    }
  ],
  "responses": {
    "200": {
      "description": "Item title is updated"
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
    }
  ],
  "responses": {
    "200": {
      "description": "Item is deleted from bucketlist"
    }
  }   
}