package DAO

type Credentials struct {
	Email   		string `gorm:"column:Email"`
	Encrypt_pasword	string `gorm:"column:Encrypt_pasword"`
   }

// This function is for GORM library which takes in the name of the database
func (Credentials) TableName() string {
	return "credentials"
   }
