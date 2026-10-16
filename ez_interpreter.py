#!/usr/bin/env python3
"""EZ Programming Language Interpreter - Version 1.0
The most intuitive, easy-to-learn programming language.
"""

import sys
import os


class EZError(Exception):
    pass


class EZInterpreter:
    def __init__(self, source_code):
        self.source = source_code
        self.lines = source_code.strip().split('\n')
        self.pos = 0
        self.variables = {}
        self.output = []

    def run(self):
        try:
            while self.pos < len(self.lines):
                line = self.lines[self.pos].strip()
                self.pos += 1
                if not line or line.startswith('#'):
                    continue
                self.execute(line)
            return self.output
        except EZError as e:
            print(f"EZ Error: {e}")
            return None

    def execute(self, line):
        parts = line.split()
        if not parts:
            return

        cmd = parts[0].lower()

        if cmd == "let":
            self._handle_let(line, parts)
        elif cmd == "print":
            self._handle_print(parts)
        elif cmd == "input":
            self._handle_input(parts)
        elif cmd == "if":
            self._handle_if(line, parts)
        elif cmd == "while":
            self._handle_while(line, parts)
        elif cmd in ("else", "end"):
            pass
        else:
            raise EZError(f"Comando desconhecido: {cmd}")

    def _parse_value(self, val_str):
        val_str = val_str.strip()
        if val_str.lower() == "true":
            return True
        if val_str.lower() == "false":
            return False
        try:
            if "." in val_str:
                return float(val_str)
            return int(val_str)
        except ValueError:
            pass
        if val_str.startswith('"') and val_str.endswith('"'):
            return val_str[1:-1]
        if val_str in self.variables or val_str.isidentifier():
            return self.variables.get(val_str, val_str)
        return val_str

    def _get_num(self, val):
        if isinstance(val, (int, float)):
            return val
        if isinstance(val, str):
            try:
                return float(val)
            except ValueError:
                pass
        raise EZError(f"Não é um número válido: {val}")

    def _eval_expr(self, expr_str):
        expr_str = expr_str.strip()
        for op in ["==", "!=", ">=", "<=", ">", "<"]:
            if op in expr_str:
                parts_expr = expr_str.split(op)
                if len(parts_expr) == 2:
                    left = self._parse_value(parts_expr[0].strip())
                    right = self._parse_value(parts_expr[1].strip())
                    return ("cmp", op, left, right)
        for op in ["+", "-", "*", "/"]:
            op_pattern = f" {op} "
            if op_pattern in expr_str:
                parts_expr = expr_str.split(op_pattern, 1)
                if len(parts_expr) == 2:
                    left = self._parse_value(parts_expr[0].strip())
                    right = self._parse_value(parts_expr[1].strip())
                    return ("arith", op, left, right)
        return ("val", self._parse_value(expr_str))

    def _eval_expr_result(self, expr_parsed):
        typ = expr_parsed[0]
        if typ == "val":
            return expr_parsed[1]
        elif typ == "arith":
            _, op, left, right = expr_parsed
            l = self._get_num(left)
            r = self._get_num(right)
            if op == "+":
                return l + r
            elif op == "-":
                return l - r
            elif op == "*":
                return l * r
            elif op == "/":
                if r == 0:
                    raise EZError("Divisão por zero")
                return l / r
        elif typ == "cmp":
            _, op, left, right = expr_parsed
            if op == "==":
                return left == right
            elif op == "!=":
                return left != right
            elif op == ">":
                return left > right
            elif op == "<":
                return left < right
            elif op == ">=":
                return left >= right
            elif op == "<=":
                return left <= right
        return expr_parsed[1]

    def _handle_let(self, line, parts):
        if len(parts) < 4 or parts[2] != "=":
            raise EZError("Sintaxe: let <variavel> = <valor>")
        var_name = parts[1]
        value_str = " ".join(parts[3:])
        expr_parsed = self._eval_expr(value_str)
        value = self._eval_expr_result(expr_parsed)
        self.variables[var_name] = value

    def _handle_print(self, parts):
        output_parts = []
        for p in parts[1:]:
            val = self._parse_value(p)
            if isinstance(val, str):
                output_parts.append(val)
            else:
                output_parts.append(str(val))
        self.output.append(" ".join(output_parts))

    def _handle_input(self, parts):
        if len(parts) < 2:
            raise EZError("Sintaxe: input <variavel>")
        var_name = parts[1]
        user_input = input("> ")
        try:
            if "." in user_input:
                self.variables[var_name] = float(user_input)
            else:
                self.variables[var_name] = int(user_input)
        except ValueError:
            self.variables[var_name] = user_input

    def _find_else_and_end(self):
        else_pos = None
        end_pos = None
        for i in range(self.pos, len(self.lines)):
            line = self.lines[i].strip().lower()
            if line == "else" and else_pos is None:
                else_pos = i
            if line == "end" and end_pos is None:
                end_pos = i
            if else_pos is not None and end_pos is not None:
                break
        return else_pos, end_pos

    def _execute_lines_range(self, start_pos, end_exclusive):
        while self.pos < len(self.lines) and self.pos < end_exclusive:
            line = self.lines[self.pos].strip()
            self.pos += 1
            if not line or line.startswith('#'):
                continue
            self.execute(line)

    def _handle_if(self, line, parts):
        condition_str = line[2:].strip()

        for op in ["==", "!=", ">=", "<=", ">", "<"]:
            if op in condition_str:
                cond_parts = condition_str.split(op)
                if len(cond_parts) == 2:
                    left = self._parse_value(cond_parts[0].strip())
                    right = self._parse_value(cond_parts[1].strip())
                    break
        else:
            raise EZError("Condição inválida. Use: ==, !=, >=, <=, >, <")

        condition_met = False
        if op == "==":
            condition_met = left == right
        elif op == "!=":
            condition_met = left != right
        elif op == ">=":
            condition_met = left >= right
        elif op == "<=":
            condition_met = left <= right
        elif op == ">":
            condition_met = left > right
        elif op == "<":
            condition_met = left < right

        else_pos, end_pos = self._find_else_and_end()

        if condition_met:
            if else_pos is None:
                self._execute_lines_range(self.pos, end_pos if end_pos else len(self.lines))
            else:
                self._execute_lines_range(self.pos, else_pos)
                if self.pos < len(self.lines) and self.lines[self.pos].strip().lower() == "else":
                    self.pos += 1
                # Advance past else block and "end"
                while self.pos < len(self.lines) and self.lines[self.pos].strip().lower() != "end":
                    self.pos += 1
                if self.pos < len(self.lines):
                    self.pos += 1
        elif else_pos is not None:
            self.pos = else_pos + 1
            self._execute_lines_range(self.pos, end_pos if end_pos else len(self.lines))
            if self.pos < len(self.lines) and self.lines[self.pos].strip().lower() == "end":
                self.pos += 1

    def _handle_while(self, line, parts):
        condition_str = line[5:].strip()

        for op in ["==", "!=", ">=", "<=", ">", "<"]:
            if op in condition_str:
                cond_parts = condition_str.split(op)
                if len(cond_parts) == 2:
                    left = self._parse_value(cond_parts[0].strip())
                    right = self._parse_value(cond_parts[1].strip())
                    break
        else:
            raise EZError("Condição inválida. Use: ==, !=, >=, <=, >, <")

        condition_met = False
        if op == "==":
            condition_met = left == right
        elif op == "!=":
            condition_met = left != right
        elif op == ">=":
            condition_met = left >= right
        elif op == "<=":
            condition_met = left <= right
        elif op == ">":
            condition_met = left > right
        elif op == "<":
            condition_met = left < right

        if condition_met:
            self._execute_lines_range(self.pos, len(self.lines))

    def _parse_condition(self, condition_str):
        for op in ["==", "!=", ">=", "<=", ">", "<"]:
            if op in condition_str:
                cond_parts = condition_str.split(op)
                if len(cond_parts) == 2:
                    left = self._parse_value(cond_parts[0].strip())
                    right = self._parse_value(cond_parts[1].strip())
                    return op, left, right
        raise EZError(f"Operador inválido: {condition_str}")


def run_ez_code(source_code):
    interpreter = EZInterpreter(source_code)
    return interpreter.run()


def repl():
    print("=== EZ Language REPL (Ctrl+D to exit) ===")
    code = []
    while True:
        try:
            line = input("ez> ")
            code.append(line)
        except EOFError:
            break
        except KeyboardInterrupt:
            print()
            break
    source = "\n".join(code)
    if source.strip():
        output = run_ez_code(source)
        if output:
            for line in output:
                print(line)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            source = f.read()
        output = run_ez_code(source)
        if output:
            for line in output:
                print(line)
    else:
        repl()
