package Controller

import (
	"../DAO"
	"fmt"
	"net/http"
	"github.com/gin-gonic/gin"
   )

// Get all users
func GetUsers(c *gin.Context) {
	// This user variable will contain all users in Credentials struct
	var user []DAO.Credentials
	err := DAO.GetAllUsers(&user)

	if err != nil {
		c.AbortWithStatus(http.StatusNotFound)
	} else {
		c.JSON(http.StatusOK, user)// User is returned here
	}
}

//Create new User
func CreateUser(c *gin.Context) {
	var user DAO.Credentials
	//Binding the json to user varaible that was given with the request
	c.BindJSON(&user)
	err := DAO.CreateUser(&user)
	if err != nil {
		fmt.Println(err.Error())
		c.AbortWithStatus(http.StatusNotFound)
	} else {
		c.JSON(http.StatusOK, user)
	}
}

//GetUserByEmail ... Get the user by emial   
func GetUserByEmail(c *gin.Context) {
	email := c.Params.ByName("email")
	var user DAO.Credentials
	err := DAO.GetUserByEmail(&user, email)
	if err != nil {
	 c.AbortWithStatus(http.StatusNotFound)
	} else {
	 c.JSON(http.StatusOK, user)
	}
}

//UpdateUser ... Update the user information
func UpdateUser(c *gin.Context) {
	var user DAO.Credentials
	email := c.Params.ByName("email")

	// Seeing if the user exists or not
	err := DAO.GetUserByEmail(&user, email)
	if err != nil {
		c.JSON(http.StatusNotFound, user)
	}

	// Deleting the user 
	err2 := DAO.DeleteUser(&user, email)
	if err2 != nil {
	 c.AbortWithStatus(http.StatusNotFound)
	} else {
	 c.JSON(http.StatusOK, gin.H{email: "is deleted"})
	}

	//Binding the json that was given in the put
	c.BindJSON(&user)

	//Create User again
	err3 := DAO.CreateUser(&user)
	if err3 != nil {
		fmt.Println(err.Error())
		c.AbortWithStatus(http.StatusNotFound)
	} else {
		c.JSON(http.StatusOK, user)
	}
}

//DeleteUser ... Delete the user
func DeleteUser(c *gin.Context) {
	var user DAO.Credentials
	email := c.Params.ByName("email")
	err := DAO.DeleteUser(&user, email)
	if err != nil {
	 c.AbortWithStatus(http.StatusNotFound)
	} else {
	 c.JSON(http.StatusOK, gin.H{"email" + email: "is deleted"}) // Return this value as a response
	}
}
