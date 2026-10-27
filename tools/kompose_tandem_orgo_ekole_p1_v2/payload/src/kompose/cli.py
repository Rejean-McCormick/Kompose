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
from .kontexte_preview import compile_preview, role_projection, propose_absence_fallback, ScenarioPreviewError
from .mission_replay import replay_receipts
from .tandem_handoff import verify_teacher_preview, TandemHandoffError

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
    preview=sub.add_parser('preview-kontexte',help='compiler sans exécuter une mission Kontexte fictive')
    preview.add_argument('mission',type=Path)
    preview.add_argument('roles_dir',type=Path)
    preview.add_argument('--target-course',default='qc-pri-ma-008')
    preview.add_argument('--role',help='projection sans secrets pour un rôle, à titre de démonstration')
    preview.add_argument('--absent-role',help='proposition de repli pour un rôle absent (sans mutation)')
    preview.add_argument('--replay',type=Path,help='rejouer des reçus Orgo fictifs pour tester les dépendances')
    preview.add_argument('--out',type=Path,help='écrire résultat JSON en fichier (facultatif)')
    tandem=sub.add_parser('verify-ekole-preview',help='Vérifier un aperçu Ekole P1 synthétique, sans Orgo')
    tandem.add_argument('file',type=Path)
    args=p.parse_args(argv)
    try:
        if args.command=='verify-ekole-preview':
            # load_json = file reader only; the verifier accepts no extra fields.
            result=verify_teacher_preview(load_json(args.file))
            print(json.dumps(result,ensure_ascii=False,indent=2))
        elif args.command=='preview-kontexte':
            mission=load_json(args.mission)
            rolefiles=sorted(args.roles_dir.glob('*.json'))
            roles=[load_json(f) for f in rolefiles]
            plan=compile_preview(mission,roles,target_course_id=args.target_course)
            result=role_projection(plan,args.role) if args.role else plan
            if args.absent_role:
                if args.role: raise ScenarioPreviewError('Repli proposé uniquement en vue enseignant')
                result={'plan':plan,'fallback':propose_absence_fallback(plan,args.absent_role)}
            if args.replay:
                if args.role:
                    raise ScenarioPreviewError('Replay détaillé réservé à la projection enseignant')
                result={'plan':plan,'replay':replay_receipts(plan,load_json(args.replay)['receipts'])}
            output=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
            if args.out:
                args.out.parent.mkdir(parents=True,exist_ok=True)
                args.out.write_text(output,encoding='utf-8')
                print(f'Aperçu synthétique écrit : {args.out}',file=sys.stderr)
            else:
                print(output,end='')
        elif args.command=='validate':
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
    except (OSError, ValueError, KeyError, PermissionError, ReferenceError, ScenarioPreviewError, TandemHandoffError) as exc:
        print(f'ERREUR: {exc}',file=sys.stderr)
        return 1

if __name__=='__main__':
    raise SystemExit(main())
