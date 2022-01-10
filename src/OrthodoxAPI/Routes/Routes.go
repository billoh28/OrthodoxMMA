package Routes

import (
	"../Controller"
	"github.com/gin-gonic/gin" // Gin is a web framework handling REST requests
   )

// Setting Router
func SetupRouter() *gin.Engine {
	r := gin.Default()
	grp1 := r.Group("/user-api") // Handling everything regarding Credentials
	{
		grp1.GET("user", Controller.GetUsers) // Get all users
		grp1.POST("user", Controller.CreateUser) // Create new user
		grp1.GET("user/:email", Controller.GetUserByEmail) // Get user by email
		grp1.PUT("user/:email", Controller.UpdateUser) // Update user password
		grp1.DELETE("user/:email", Controller.DeleteUser) // Delete user
		
	}
	grp2 := r.Group("/user-api-feedback") // Handling everything regarding Feedback Reports
	{
		grp2.GET("user/:email", Controller.GetAllFeedbacks) // Get all feedback reports
		grp2.POST("user", Controller.CreateFeedback) // Create new feedback report
	}
	return r
}