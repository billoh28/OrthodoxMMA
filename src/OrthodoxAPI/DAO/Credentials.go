package DAO

import (
	"../Config"
	// "fmt"
	_ "github.com/go-sql-driver/mysql"
   )

//GetAllUsers Fetch all user data
func GetAllUsers(user *[]Credentials) (err error) {
	if err = Config.DB.Find(user).Error; err != nil {
	 return err
	}
	return nil
   }

//CreateUser ... Insert New data
func CreateUser(user *Credentials) (err error) {
	err = Config.DB.Create(user).Error;
	if err != nil {
		return err
	}
	return nil
   }

//GetUserByemail ... Fetch only one user by email
func GetUserByEmail(user *Credentials, email string) (err error) {
	if err = Config.DB.Where("email = ?", email).First(user).Error; err != nil {
		return err
	}
	return nil
   }

//UpdateUser ... Update user   
func UpdateUser(user *Credentials, email string) (err error) {
	Config.DB.Save(user)
	return nil
   }

//DeleteUser ... Delete user   
func DeleteUser(user *Credentials, email string) (err error) {
	Config.DB.Where("email = ?", email).Delete(user)
	return nil
   }