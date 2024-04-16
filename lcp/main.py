# -*- coding: utf-8 -*-

import argparse
import os
import sys
import json


def main():
    parser = argparse.ArgumentParser(
        description='LCP: Load Container Problem')
    parser.add_argument('command', choices=['generate', 'solve', 'visualize'],
                        help='Comando a ejecutar')
    parser.add_argument('file', type=str,
                        help='Archivo de entrada')
    parser.add_argument('-o', '--output', type=str,
                        help='Archivo de salida')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Mostrar información adicional')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Mostrar información de depuración')
    args = parser.parse_args()

    if args.command == 'generate':
        if args.verbose:
            print("Generando datos...")
        generate(args.file, args.output)
    elif args.command == 'solve':
        if args.verbose:
            print("Resolviendo...")
        solve(args.file, args.output)
    elif args.command == 'visualize':
        if args.verbose:
            print("Visualizando...")
        visualize(args.file, args.output)
