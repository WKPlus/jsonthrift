struct returnType{
1:i32 index
2:string istrue
}

struct Complex{
1:bool param_bool
2:byte param_byte
3:i16 param_i16
4:i32 param_i32
5:i64 param_i64
6:double param_double
7:string param_str
8:list<i64> param_list_i64
9:list<list<string>> param_list_list
10:list<list<list<i32>>> param_list_list_list
11:list<list<returnType>> param_list_list_class
12:list<list<map<string, string>>> param_list_list_map
13:list<list<set<string>>> param_list_list_set
14:list<set<i32>> param_list_set_basic
15:list<set<list<byte>>> param_set_list_byte
16:map<string, bool> param_map_str_bool
17:map<string, byte> param_map_str_byte
18:map<string, i16> param_map_str_i16
19:map<string, i32> param_map_str_i32
20:map<string, map<string, list<bool>>> param_map_str_map_list
21:map<string, map<string, map<string, i64>>> param_map_str_map_map
22:map<string, map<string, set<i32>>> param_map_str_map_set
23:map<i32, returnType> param_map_i32_class
24:set<byte> param_set_byte
25:set<i16> param_set_i16
26:set<i64> param_set_i64
27:set<returnType> param_set_class
28:set<map<string, double>> param_set_map_double
29:set<set<double>> param_set_set
30:returnType param_class
}
service TestService{
returnType test_call(1:required list<Complex> param)
}
