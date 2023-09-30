package models

type Resource struct {
	Url      string `json:"url"`
	Name     string `json:"name"`
	IsFree   string `json:"is_free"`
	IsActive string `json:"is_active"`
}
