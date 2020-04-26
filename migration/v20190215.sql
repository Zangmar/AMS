-- 导入员工

INSERT INTO employee_info (phone, password, permission, name, department, is_work)
SELECT 
	s.staff_telephone, '', 1, s.staff_name, d.department_name, '1'
from 
  staff_all AS s INNER JOIN department_all AS d
ON 
  s.department_id=d.department_number;