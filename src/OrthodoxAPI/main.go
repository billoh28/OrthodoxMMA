package main

import (
	"../OrthodoxAPI/Config"
	"../OrthodoxAPI/DAO"
	"../OrthodoxAPI/Routes"
	"fmt"
	"github.com/jinzhu/gorm" // Googles object relational mapping for databases
   )

var err error

func main() {
	Config.DB, err = gorm.Open("mysql", Config.DbURL()) // Create a database instance
		
	if err != nil {
		fmt.Println("Status:", err) // For logging
	}
	
	defer Config.DB.Close()
	
	Config.DB.AutoMigrate(&DAO.Credentials{}) // Automatically migrate Credenitals struct schema, to keep your schema up to date
	Config.DB.AutoMigrate(&DAO.Feedback{}) // Same for Feedback struct


	r := Routes.SetupRouter() // Sets up all REST commands
	r.Run()
   }