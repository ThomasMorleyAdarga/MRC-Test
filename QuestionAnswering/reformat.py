import argparse
import json


def main(train, test, val, data):

    # Dict to hold current dataset
    og_dataset = dict.fromkeys(('train', 'test', 'val'))

    # First open Json files
    with open(train, 'r') as f:
        og_dataset['train'] = json.load(f)
        f.close()
    with open(test, 'r') as f:
        og_dataset['test'] = json.load(f)
        f.close()
    with open(val, 'r') as f:
        og_dataset['val'] = json.load(f)
        f.close()

    # Create new dictionary
    final_output = dict.fromkeys(('train', 'test', 'val'))
    final_output['train'], final_output['test'], final_output['val'] = list(), list(), list()

    # Generate final examples
    for f in ['train', 'test', 'val']:
        for example in og_dataset[f]:

            # Unused variables set to none
            doc_id = None
            entity_head_list = None
            ner_total_list = None
            pos = None

            # text = words list
            text = example['words']

            # event_list = BIO for events
            event_list = list()
            for i, word in enumerate(text):
                for event in example['golden-event-mentions']:
                    if i == event['trigger']['start']:
                        event_list.append(str('B-' + event['event_type']))
                    elif i > event['trigger']['start'] and i < event['trigger']['end']:
                        if i + event['trigger']['start'] < event['trigger']['start'] + len(event['trigger']['text'].split(' ')):
                            print(i, "\t", event)
                            event_list.append(str('I-' + event['event_type']))
                    else:
                        event_list.append('O')

            # events = dict [key = event-sub-type : value = event-arguments]
            events = {}
            for event in example['golden-event-mentions']:
                for arg in event['arguments']:
                    events.setdefault(event['event_type'].split(':')[1], list())
                    events[event['event_type'].split(':')[1]].append([arg['role'], arg['text']])

            # related entities = dict [text : {type, pos_tag, syntax_label, gov_idx, start, end}] for all golden entities
            related_entities = {}
            for entity in example['golden-entity-mentions']:

                text, entity_type, start, end = entity['text'], entity['entity-type'], entity['start'], entity['end']
                related_entities.setdefault(text, list())
                entity_data = list()


                entity_data.append(entity_type)
                '''
                entity_data.append(example['pos-tags'][start])
                if start <= int(example['stanford-colcc'][-1].split('/')[1].split('=')[1]):
                    entity_data.append(example['stanford-colcc'][start].split('/')[0])
                    entity_data.append(int(example['stanford-colcc'][start].split('/')[2].split('=')[1]))
                else:
                    entity_data.append(None)
                    entity_data.append(None)
                '''
                entity_data.extend([None, None, None])
                entity_data.append(start)
                entity_data.append(end)

                related_entities[entity['text']] = entity_data

            final_output[f].append([ doc_id, text, entity_head_list, ner_total_list, event_list, events, pos, related_entities])


    # write result to output file
    with open(data, 'w') as f:
        json.dump(final_output, f)
        f.close()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='egnn for ed')

    parser.add_argument('train', default="", type=str)
    parser.add_argument('test', default="", type=str)
    parser.add_argument('val', default="", type=str)
    parser.add_argument('data', default="", type=str)

    args = parser.parse_args()

    train = args.train
    test = args.test
    val = args.val
    data = args.data

    main(train, test, val, data)