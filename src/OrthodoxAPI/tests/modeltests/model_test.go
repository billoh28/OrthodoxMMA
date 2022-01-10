package modeltests

import (
	"fmt"
	"log"
	// "os"
	// "testing"

	"github.com/jinzhu/gorm"
	// "github.com/joho/godotenv"
	// "../../Controller"
	"../../DAO"
	"../../Config"
)

type Server struct {
	DB     *gorm.DB
}

var server = Server{}
var CredInstance = DAO.Credentials{}
var FBInstance = DAO.Feedback{}

func Database() {
	var err error
	DBURL := fmt.Sprintf("%s:@tcp(%s:%s)/%s?charset=utf8&parseTime=True&loc=Local", "root", "localhost", "3306", "test")
	if server.DB, err = gorm.Open("mysql", DBURL); err != nil {
		fmt.Printf("Cannot connect to %s database", "mysql")
	} else {
		fmt.Printf("We are connected to the %s database", "mysql")
	}
}

func refreshALLTable() error {
	err := Config.DB.DropTableIfExists(&DAO.Credentials{}, &DAO.Feedback{}).Error
	if err != nil {
		return err
	}
	err = Config.DB.AutoMigrate(&DAO.Credentials{}, &DAO.Feedback{}).Error
	if err != nil {
		return err
	}
	log.Printf("Successfully refreshed tables")
	return nil
}

func seedOneCred() (error) {

	refreshALLTable()

	cred := DAO.Credentials{
		Email:    "Testing@gmail.com",
		Encrypt_pasword: "password1234",
	}


	err := Config.DB.Model(&DAO.Credentials{}).Create(&cred).Error
	if err != nil {
		log.Fatalf("cannot seed users table: %v", err)
	}
	return nil
}

func seedOneFeedB() (error) {

	refreshALLTable()

	feedback := DAO.Feedback{
		Email:    "testing@gmail.com",
		Feedback: "This is your feedback",
	}

	err := Config.DB.Model(&DAO.Feedback{}).Create(&feedback).Error
	if err != nil {
		log.Fatalf("cannot seed users table: %v", err)
	}
	return nil
}