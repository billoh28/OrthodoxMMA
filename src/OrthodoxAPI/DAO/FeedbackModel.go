package DAO

type Feedback struct {
	Email  string `gorm:"column:Email"`
	Feedback  string `gorm:"column:Feedback"`
}

// This function is for GORM library which takes in the name of the database
func (Feedback) TableName() string {
	return "feedbacks"
   }