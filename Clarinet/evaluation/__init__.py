import json
import os
import miditoolkit
from tqdm import tqdm
from Clarinet.search.similarity_time import midiEt_to_note_sequence, midiEt_to_note, splitNotes, getStrides
from Clarinet.search import similarity, Note


factor = 768


def evaluate(query_json, data_json, output_file="res", similarity_algo="text"):
    with open(data_json, 'r') as f:
        fname_to_notes = json.load(f)
    with open(query_json, 'r') as f:
        query_to_notes = json.load(f)

    res = {}
    for query_name, query_notes in tqdm(query_to_notes.items()):
        qnotes = [note[0] for note in query_notes]
        query = midiEt_to_note_sequence(qnotes)
        fname_to_similarity = {}
        if similarity_algo == "sankoff":
            qrep = []
            prev_end = 0
            for n in notes:
                if n[1] > prev_end:
                    qrep.append(Note("C", int((n[1]-prev_end)/t), rest=True))
                qrep.append(Note(midiEt_to_note[n[0] % 12 + 12], int((n[2]-n[1])/t), rest=False))
                prev_end = n[2]

        for fname in fname_to_notes:
            sim = 0
            notes = fname_to_notes[fname]

            if similarity_algo == "time":
                notes = splitNotes(notes)
                strides = getStrides(notes, 5*factor)
                for stride in strides:
                    stride_notes = [note[0] for note in stride]
                    note_sequence = midiEt_to_note_sequence(stride_notes)
                    sim = max(sim, similarity(query, note_sequence, similarity_algo))

            elif similarity_algo == "text":
                nn = []
                for n in notes:
                    nn.append(n[0])
                note_sequence = midiEt_to_note_sequence(nn)
                sim = max(sim, similarity(query, note_sequence, similarity_algo))

            elif similarity_algo == "sankoff":
                #end_time = notes[-1][2]
                #tempo = 120
                #t = end_time/(4*tempo)
                t = 500
                rep = []
                prev_end = 0
                for n in notes:
                    if n[1] > prev_end:
                        rep.append(Note("C", int((n[1]-prev_end)/t), rest=True))
                    rep.append(Note(midiEt_to_note[n[0] % 12 + 12], int((n[2]-n[1])/t), rest=False))
                    prev_end = n[2]
                sim = similarity(qrep, rep, similarity_algo)
            fname_to_similarity[fname] = sim

        fname_to_similarity = dict(sorted(fname_to_similarity.items(), key=lambda item: item[1], reverse=True))
        res[query_name] = fname_to_similarity
    if output_file == "res":
        output_file = f"res_{similarity_algo}.json"

    with open(output_file, 'w') as f:
        json.dump(res, f)


if __name__ == "__main__":
    evaluate(r"C:\Users\Kshitij Alwadhi\Documents\GitHub\Clarinet\Data\Json\2018_queries\melody.json", r"C:\Users\Kshitij Alwadhi\Documents\GitHub\Clarinet\Data\Json\2018_clipped\melody.json", similarity_algo="text")
