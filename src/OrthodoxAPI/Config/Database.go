package Config

import (
	"fmt"
	"github.com/jinzhu/gorm"
	"gopkg.in/yaml.v2"
	"io/ioutil"
)

var DB *gorm.DB // Database instance

// Struct of the Configuration file for the database
type Configs struct {
	DBConfigs struct {
		Host string `yaml:"Host"`
		Port int `yaml:"Port"` 
		User string `yaml:"User"`
		DBName string `yaml:"DBName"`
		Password string `yaml:"Password"`
	} `yaml:"DBConfigs"`
}

// Reading in the yaml file	
func GetConf(filename string) (*Configs, error) {

	yamlFile, err := ioutil.ReadFile(filename)

	if err != nil {
		fmt.Printf("yamlFile.Get err : #%v", err)
	}

	var conf Configs
	err = yaml.Unmarshal(yamlFile, &conf) // Converts yaml format into Configs struct above

	if err != nil {
		fmt.Printf("Unmarshal : #%v", err)
	}
	return &conf, nil
}

// Returns Database URL for sql to connect to
func DbURL() string {

	conf, err := GetConf("Config/configuration.yml") // Calls on yaml file
	if err != nil {
		fmt.Printf("GetConf : #%v", err)
	}

	return fmt.Sprintf(
		"%s:%s@tcp(%s:%d)/%s?charset=utf8&parseTime=True&loc=Local",
		conf.DBConfigs.User,
		conf.DBConfigs.Password,
		conf.DBConfigs.Host,
		conf.DBConfigs.Port,
		conf.DBConfigs.DBName,
	)
}