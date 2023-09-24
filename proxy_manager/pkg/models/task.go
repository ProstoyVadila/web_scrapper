package models

type Task struct {
	Func     func()
	Interval string
	Name     string
}

func NewTask(name, interval string) *Task {
	return &Task{
		Interval: interval,
		Name:     name,
	}
}

func (t *Task) SetFunc(f func()) {
	t.Func = f
}
