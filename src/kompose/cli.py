"""CLI de validation et de démonstration en local (pas une API KOMPOSE)."""
import argparse
import json
import sys
from pathlib import Path
from .validation import load_json, validate_directory, ReferenceError
from .reader import read_answer
from .events import select_prompts
from .allocation_policy import first_choice_quota
from .demo import run_demo
from .coordination import ready_missions

def main(argv=None):
    p=argparse.ArgumentParser(description='KOMPOSE : contrats et démonstrateur documentaire sans IA')
    sub=p.add_subparsers(dest='command',required=True)
    v=sub.add_parser('validate',help='vérifier une capsule locale')
    v.add_argument('directory',type=Path)
    r=sub.add_parser('read',help='lire une réponse préécrite')
    r.add_argument('file',type=Path);r.add_argument('kristal_id');r.add_argument('topic_id');r.add_argument('question_id')
    r.add_argument('--demo',action='store_true',help='autoriser explicitement contenus fictifs de démonstration')
    t=sub.add_parser('trigger',help='simuler un événement vers les prompts')
    t.add_argument('file',type=Path);t.add_argument('event');t.add_argument('--audience',default='demandeur');t.add_argument('--demo',action='store_true')
    q=sub.add_parser('quota');q.add_argument('nombre',type=int)
    d=sub.add_parser('demo-flow', help='simuler une capsule entière avec données fictives')
    d.add_argument('directory',type=Path)
    m=sub.add_parser('ready-missions', help='missions débloquées selon les dépendances')
    m.add_argument('file',type=Path)
    m.add_argument('--completed', nargs='*', default=[])
    args=p.parse_args(argv)
    try:
        if args.command=='validate':
            errors=validate_directory(args.directory)
            if errors:
                for e in errors:print('ERREUR:',e,file=sys.stderr)
                return 1
            print('OK : références croisées, statut démo, sécurité éditoriale et exemple cohérents.')
        elif args.command=='read':
            if args.demo:print('ATTENTION : texte fictif, non historique, usage de démonstration seulement.',file=sys.stderr)
            ks=load_json(args.file)['kristals']
            # Le CLI simule un droit d'accès local; ce drapeau ne vaut pas autorisation réelle.
            result=read_answer(ks,args.kristal_id,args.topic_id,args.question_id,access_granted=True,demo=args.demo)
            print(json.dumps(result,ensure_ascii=False,indent=2))
        elif args.command=='trigger':
            if not args.demo:
                raise PermissionError('Simulation des prompts réservée au mode --demo')
            prompts=load_json(args.file)['prompts']
            messages,_=select_prompts(prompts,args.event,args.audience,'evt-demo','participant-demo')
            print(json.dumps(messages,ensure_ascii=False,indent=2))
        elif args.command=='quota':
            print(first_choice_quota(args.nombre))
        elif args.command=='demo-flow':
            print(json.dumps(run_demo(args.directory),ensure_ascii=False,indent=2))
        elif args.command=='ready-missions':
            missions=load_json(args.file)['missions']
            print(json.dumps(ready_missions(missions,args.completed),ensure_ascii=False,indent=2))
        return 0
    except (OSError, ValueError, KeyError, PermissionError, ReferenceError) as exc:
        print(f'ERREUR: {exc}',file=sys.stderr)
        return 1

if __name__=='__main__':
    raise SystemExit(main())
