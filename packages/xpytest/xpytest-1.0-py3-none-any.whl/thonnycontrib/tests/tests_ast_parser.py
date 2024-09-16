from typing import List
import unittest, ast

from thonnycontrib.backend.ast_parser import L1DocTest, L1TestAstParser
from thonnycontrib.backend.doctest_parser import ExampleExceptionExpected, ExampleFactory, ExampleWithExpected, ExampleWithoutExpected

class TestL1TestAstParser(unittest.TestCase):

    def setUp(self):
        self.parser = L1TestAstParser()
        
    def tearDown(self):
        self.parser = None
    
    ### ########################## ###
    ### ---- Integration tests --- ###
    ### Tests for the parse method ###
    ### ########################## ###
    
    # Test to check if the parse method correctly extracts L1DocTests
    def test_parse_with_doctest(self):
        source = \
"""\
def foo():
    '''
    This is a docstring.
    
    $$$ a = 1
    $$$ b = 2
    $$$ a + b
    3
    '''
    pass
"""
        self.parser.set_source(source)
        results = list(self.parser.parse())
        self.assertTrue(len(results) > 0)
        self.assertTrue(isinstance(results[0], L1DocTest))
    
    # Test to check if the parse method returns nothing when there's no doctest
    def test_parse_without_doctest(self):
        source = \
"""\
def foo():
    pass
"""
        self.parser.set_source(source)
        results = list(self.parser.parse())
        self.assertEqual(len(results), 1) # the L1doctest is created 
        self.assertEqual(len(results[0].get_examples()), 0) # but it contains no example
        self.assertEqual(results[0].get_start_end_lineno(), (-1, -1)) # and the start and end line numbers are -1 (because no docstring)
        

    # Test to check if the parse method correctly identifies a specific node from its line number
    def test_parse_with_line_number(self):
        source = \
"""\
def foo():
    '''
    This is a docstring.
    
    $$$ a = 1
    $$$ b = 2
    $$$ a + b
    3
    '''
    pass
    
def bar():
    '''
    Another docstring.
    
    $$$ x = 10
    $$$ y = 20
    $$$ x * y
    200
    '''
    pass
"""
        self.parser.set_source(source)
        results = list(self.parser.parse(lineno=12)) # we want the L1doctest that contains the node at line 12 (the bar() function)
        self.assertEqual(len(results), 1) # only one L1doctest is created
        self.assertEqual(results[0].get_name(), "bar()") # the name of the L1doctest is "bar()"
        self.assertEqual(results[0].get_node_lineno(), 12) # the line number of the node is 12
        self.assertEqual(results[0].get_start_end_lineno(), (13, 20)) # the start and end line numbers are 13 and 20 (because the docstring is at line 13)
        

    # Test to check if the parse method raises compilation error on invalid source
    def test_parse_invalid_source(self):
        source = \
"""\
def foo():
pass  # This is an indentation error
"""
        self.parser.set_source(source)
        with self.assertRaises(Exception):
            list(self.parser.parse())
            
    
    # Test to check if the parse method correctly handles nested functions
    def test_parse_nested_functions(self):
        source = \
"""\
def outer():
    '''
    Outer function
    
    $$$ outer_val = 5
    '''
    def inner():
        '''
        Inner function
        
        $$$ inner_val = 10
        '''
        pass
"""
        self.parser.set_source(source)
        results = list(self.parser.parse())
        self.assertEqual(len(results), 2)   
        
        
    # Test to check if the parse method correctly handles class methods
    def test_parse_class_methods(self):
        source = \
"""\
class MyClass:
    '''
    This is a class.
    
    $$$ c = MyClass()
    '''
    
    def my_method(self):
        '''
        This is a method
        
        $$$ m = 5
        $$$ m * 2
        10
        '''
        pass
"""
        self.parser.set_source(source)
        results = list(self.parser.parse()) 
        self.assertEqual(len(results), 2)
    
    
    # Test to check if the parse method correctly handles unsupported nodes (ex. with a simple print statement)
    def test_parse_unsupported_nodes(self):
        source = "print('Hello, World!')"
        self.parser.set_source(source)
        results = list(self.parser.parse())
        self.assertEqual(len(results), 0)  # Since there's no function or class
        
        
    # Test to check if the parse method correctly handles multiple docstrings in a function
    def test_multiple_docstrings_in_function(self):
        source = \
"""\
def func():
    '''
    This is the first docstring
    $$$ True and True
    True
    '''
    
    '''
    This is the second docstring
    
    $$$ 1 + 1
    6
    '''
    pass
"""
        self.parser.set_source(source)
        results = list(self.parser.parse())
        
        self.assertEqual(len(results), 1)  # only the first docstring is parsed
        self.assertEqual(results[0].get_start_end_lineno(), (2, 6))  # the start and end line numbers are 2 and 6 (because the first docstring is at line 2)
        
        self.assertEqual(len(results[0].get_examples()), 1)  # the first docstring contains one example
        self.assertEqual(results[0].get_examples()[0].source, "True and True\n") # the source of the example is "True and True"
        self.assertEqual(results[0].get_examples()[0].want, "True\n") # the expected result of the example is "True"
        
        
    def __create_and_add_example_to_l1doctest(self, l1doctest:L1DocTest, source:str, want:str, invite:str, lineno:int, indent:int=4):
        """
        Creates an Example and adds it to the given L1DocTest. The Example is created with the given parameters.
        The function uses the factory method ExampleFactory to create the Example. 
        See ExampleFactory for more details.
        
        Args:
            l1doctest (L1DocTest): The L1DocTest to which the Example will be added
            source (str): the source of the test
            want (str): the expected result of the test
            invite (str): the invite command that precedes the test (ex. "$$$ " or "$$e ")
            lineno (int): the line number where the test is located
            indent (int): the indentation of the test (default is 4)

        Returns:
            Example: the created Example.
        """
        example = ExampleFactory(invite, filename=self.parser.get_filename(), source=source, want=want, lineno=lineno, indent=indent, exc_msg=None, options={})
        l1doctest.add_example(example)
        return example 
    
    
    ### ########################### ###
    ### ---- Unit tests --- ###
    ### Tests for the __recursive_walking method ###
    ### ########################### ###
    
    # ce test vérifie que si la liste des noeuds est vide alors aucun l1doctest n'est créé
    def test_from_ast_to_l1doctest_when_empty_body(self):
        l1doctests = list(self.parser._L1TestAstParser__recursive_walking(list_nodes=[]))
        self.assertEqual(l1doctests, [])


    # ce test vérifie que le L1doctest est bien créé et contient un Example de type ExampleWithoutExpected
    def test_from_ast_to_l1doctest_when_a_supported_ast_node_exists_and_check_ExampleWithoutExpected(self):
        source = \
"""\
def f(a, b):
    '''
    $$$ a = f(1, 2)
    '''
    return a + b
""" 
        list_nodes = ast.parse(source, self.parser.get_filename(), mode=self.parser.get_mode()).body
        l1doctests: List[L1DocTest] = list(self.parser._L1TestAstParser__recursive_walking(list_nodes))
        
        self.assertTrue(l1doctests != [])
        self.assertTrue(len(l1doctests) == 1)
        
        expected_l1doctest = L1DocTest(filename=self.parser.get_filename(), name="f(a, b)", type="FunctionDef", node_lineno=1, start_lineno=2, end_lineno=4)
        self.__create_and_add_example_to_l1doctest(expected_l1doctest, source="a = f(1, 2)", want="", invite="$$$ ", lineno=3)
        self.assertEqual(l1doctests[0], expected_l1doctest)
        
        self.assertEqual(len(l1doctests[0].get_examples()), 1)
        self.assertEqual(l1doctests[0].get_examples()[0].__class__, ExampleWithoutExpected)
        
        
    # ce test vérifie que le L1doctest est bien créé et contient un Example de type ExampleWithExpected
    def test_from_ast_to_l1doctest_when_a_supported_ast_node_exists_and_check_ExampleWithExpected(self):
        source = \
"""\
def f(a, b):
    '''
    $$$ f(1, 2)
    3
    '''
    return a + b
""" 
        list_nodes = ast.parse(source, self.parser.get_filename(), mode=self.parser.get_mode()).body
        l1doctests: List[L1DocTest] = list(self.parser._L1TestAstParser__recursive_walking(list_nodes))
        
        self.assertTrue(l1doctests != [])
        self.assertTrue(len(l1doctests) == 1)
        
        expected_l1doctest = L1DocTest(filename=self.parser.get_filename(), name="f(a, b)", type="FunctionDef", node_lineno=1, start_lineno=2, end_lineno=5)
        self.__create_and_add_example_to_l1doctest(expected_l1doctest, source="f(1, 2)", want="3", invite="$$$ ", lineno=3)
        self.assertEqual(l1doctests[0], expected_l1doctest)
        
        self.assertEqual(len(l1doctests[0].get_examples()), 1)
        self.assertEqual(l1doctests[0].get_examples()[0].__class__, ExampleWithExpected)
    
    
    # ce test vérifie que le L1doctest est bien créé et contient un Example de type ExampleExceptionExpected
    def test_from_ast_to_l1doctest_when_a_supported_ast_node_exists_and_check_ExampleExceptionExpected(self):
        source = \
"""\
def f(a, b):
    '''
    $$e f(1, 2)
    Exception
    '''
    raise Exception("error")
""" 
        list_nodes = ast.parse(source, self.parser.get_filename(), mode=self.parser.get_mode()).body
        l1doctests: List[L1DocTest] = list(self.parser._L1TestAstParser__recursive_walking(list_nodes))
        
        self.assertTrue(l1doctests != [])
        self.assertTrue(len(l1doctests) == 1)
        
        expected_l1doctest = L1DocTest(filename=self.parser.get_filename(), name="f(a, b)", type="FunctionDef", node_lineno=1, start_lineno=2, end_lineno=5)
        self.__create_and_add_example_to_l1doctest(expected_l1doctest, source="f(1, 2)", want="Exception", invite="$$e ", lineno=3)
        self.assertEqual(l1doctests[0], expected_l1doctest)
        
        self.assertEqual(len(l1doctests[0].get_examples()), 1)
        self.assertEqual(l1doctests[0].get_examples()[0].__class__, ExampleExceptionExpected)
        
        
    # Ce test vérifie le numéro de ligne où commence le docstring dans le cas où il y a des espaces avant le docstring
    def test_from_ast_to_l1doctest_when_theres_space_before_docstring(self): 
        source = \
"""\
def f(a, b):


    '''
    $$$ f(1, 2)
    3
    '''
    return a+b
""" 
        list_nodes = ast.parse(source, self.parser.get_filename(), mode=self.parser.get_mode()).body
        l1doctests: List[L1DocTest] = list(self.parser._L1TestAstParser__recursive_walking(list_nodes))
        
        self.assertTrue(l1doctests != [])
        self.assertTrue(len(l1doctests) == 1)
        
        expected_l1doctest = L1DocTest(filename=self.parser.get_filename(), name="f(a, b)", type="FunctionDef", node_lineno=1, start_lineno=4, end_lineno=7)
        self.__create_and_add_example_to_l1doctest(expected_l1doctest, source="f(1, 2)", want="3", invite="$$$ ", lineno=5)
        self.assertEqual(l1doctests[0], expected_l1doctest)
        
        self.assertEqual(len(l1doctests[0].get_examples()), 1)
    
    
    # Ce test vérifie: si aucune doctsring n'est contenue dans un noeud ast alors le L1DocTest extrait ne contiendra aucun Example
    def test_from_ast_to_l1doctest_when_a_supported_ast_node_exists_and_has_no_docstring(self):
        source = \
"""\
def f(a, b):
    return a + b
"""
        list_nodes = ast.parse(source, self.parser.get_filename(), mode=self.parser.get_mode()).body
        l1doctests: List[L1DocTest] = list(self.parser._L1TestAstParser__recursive_walking(list_nodes))
        self.assertTrue(l1doctests != [])
        self.assertTrue(len(l1doctests) == 1)
        
        expected_l1doctest = L1DocTest(filename=self.parser.get_filename(), name="f(a, b)", type="FunctionDef", node_lineno=1, start_lineno=-1, end_lineno=-1)
        
        self.assertEqual(l1doctests[0], expected_l1doctest)
        self.assertEqual(expected_l1doctest.get_examples(), [])

    
    # test when is a non supported ast node -> no L1DocTest is created
    def test_from_ast_to_l1doctest_when_a_non_supported_ast_node_exists(self):
        source = \
"""\
async def f(a, b):
    return a + b
"""
        list_nodes = ast.parse(source, self.parser.get_filename(), mode=self.parser.get_mode()).body
        l1doctests: List[L1DocTest] = list(self.parser._L1TestAstParser__recursive_walking(list_nodes))
        self.assertTrue(l1doctests == [])
    
    
    # ce test vérifie : si des commentaires sont inclus dans les tests d'un L1doctest alors ils sont ignorés
    def test_from_ast_to_l1doctest_when_a_supported_ast_node_exists_and_check_ExampleWithoutExpected_and_ignore_comments(self):
        source = \
"""\
def f(a, b):
    '''
    $$$ f(1, 2)    # some somment here (will be ingored)
    3
    '''
    return a + b
"""
        list_nodes = ast.parse(source, self.parser.get_filename(), mode=self.parser.get_mode()).body
        l1doctests: List[L1DocTest] = list(self.parser._L1TestAstParser__recursive_walking(list_nodes))
        
        self.assertTrue(l1doctests != [])
        self.assertTrue(len(l1doctests) == 1)
        
        expected_l1doctest = L1DocTest(filename=self.parser.get_filename(), name="f(a, b)", type="FunctionDef", node_lineno=1, start_lineno=2, end_lineno=5)
        # the value of the source parameter will not contain the comment. It will be "f(1, 2)" 
        self.__create_and_add_example_to_l1doctest(expected_l1doctest, source="f(1, 2)", want="3", invite="$$$ ", lineno=3)
        self.assertEqual(l1doctests[0], expected_l1doctest)
    
    
if __name__ == "__main__":
    unittest.main(verbosity=2)