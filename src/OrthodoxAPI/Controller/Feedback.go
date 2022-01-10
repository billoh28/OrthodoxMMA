package Controller

import (
	"../DAO"
	"fmt"
	"net/http"
	"github.com/gin-gonic/gin"
   )


//Get all Feedbacks given an email address
func GetAllFeedbacks(c *gin.Context) {
	email := c.Params.ByName("email")
	var reportobj []DAO.Feedback
	
	err := DAO.GetAllFeedbacks(&reportobj, email) // Call data access object

	if err != nil {
		c.AbortWithStatus(http.StatusNotFound)
	} else {
		c.JSON(http.StatusOK, reportobj)
	}
}

//Create a new feedback report given json of email and report dictionary
func CreateFeedback(c *gin.Context) {
	var reportobj DAO.Feedback
	// Bind reportobj to the given json
	c.BindJSON(&reportobj)
	err := DAO.CreateFeedback(&reportobj)
	if err != nil {
		fmt.Println(err.Error())
		c.AbortWithStatus(http.StatusNotFound)
	} else {
		c.JSON(http.StatusOK, reportobj)
	}
}