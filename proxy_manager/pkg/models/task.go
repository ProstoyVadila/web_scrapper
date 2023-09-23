package models

type Task interface {
	SetFunc(f func())
}

type TemplateTask struct {
	Func     func()
	Interval string
	Name     string
}

func NewTask(name, interval string) *TemplateTask {
	return &TemplateTask{
		Interval: interval,
		Name:     name,
	}
}

func (t *TemplateTask) SetFunc(f func()) {
	t.Func = f
}
