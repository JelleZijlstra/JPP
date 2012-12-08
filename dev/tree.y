%{
// Yacc input grammar for trees, used in the implementation of tree_parse.py

%}
%union {
	int iValue;
};
%token <iValue> T_DIGIT

%%
program:
	tree	{}
;

tree:
	T_DIGIT	{}
	| '(' tree ',' tree ')'	{}
;

%%
