package modeltests

import (
	"log"
	"testing"

	_ "github.com/jinzhu/gorm/dialects/mysql"    //mysql driver
	// "github.com/victorsteven/fullstack/api/models"
	// "../../DAO"
	"../../Config"
	"gopkg.in/go-playground/assert.v1"

)

func TestFindAllCreds(t *testing.T) {

	err := refreshALLTable()
	if err != nil {
		log.Fatal(err)
	}

	err = seedOneCred()
	if err != nil {
		log.Fatal(err)
	}

	cred, err := CredInstance.GetAllUsers(Config.DB)
	if err != nil {
		t.Errorf("this is the error getting the creds: %v\n", err)
		return
	}
	assert.Equal(t, len(*cred), 2)
}