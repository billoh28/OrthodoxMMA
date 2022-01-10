package DAO

import (
	"../Config"
	_ "github.com/go-sql-driver/mysql" // Importing side effects: Not being used for its init but for its other utilities
   )

// Get all feedback reports given a users email address for the reports page 
func GetAllFeedbacks(reportobj *[]Feedback, email string) (err error) {
	Config.DB.Raw("SELECT Email, Feedback FROM feedbacks WHERE Email = ?", email).Scan(&reportobj)
	return nil
   }


//Create a feedback report
func CreateFeedback(reportobj *Feedback) (err error) {
	err = Config.DB.Create(reportobj).Error;
	if err != nil {
		return err
	}
	return nil
   }
