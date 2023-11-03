use ttf2mesh::{Quality, TTFFile, Value};
use std::fs::File;
use std::io::Read;

fn main() {
    let mut font_file = File::open("../font/NotoSansJP-SemiBold.ttf").unwrap();
    let mut buf = vec![];
    font_file.read_to_end(&mut buf).unwrap();
    let mut font = TTFFile::from_buffer_vec(buf).unwrap();

    for char in "Hello_World".chars() {
        let mut glyph = font.glyph_from_char(char).unwrap();
        let mesh = glyph.to_2d_mesh(Quality::Medium).unwrap();

        println!("Mesh data char {:?}", char);
        println!(
            "- vertices: [{}]",
            mesh.iter_vertices()
                .map(|v| {
                    let v = v.val();
                    format!("({:.3}, {:.2})", v.0, v.1)
                })
                .collect::<Vec<_>>()
                .join(", ")
        );
        println!(
            "- faces: [{}]",
            mesh.iter_faces()
                .map(|v| {
                    let v = v.val();
                    format!("({}, {}, {})", v.0, v.1, v.2)
                })
                .collect::<Vec<_>>()
                .join(", ")
        );
        println!("");


        let scale = 20.0;
        let vertices = mesh.iter_vertices().map(|v| {
            let v = v.val();
            (v.0 * scale, -v.1 * scale + scale)
        }).collect::<Vec<_>>();
        println!("<svg width=\"1000\" height=\"1000\" viewBox=\"0 -{0} {0} {0}\" xmlns=\"http://www.w3.org/2000/svg\">", scale);
        for face in mesh.iter_faces() {
            let face = face.val();
            // svg polygon
            println!("<polygon points=\"{},{} {},{} {},{}\" />", vertices[face.0 as usize].0, vertices[face.0 as usize].1, vertices[face.1 as usize].0, vertices[face.1 as usize].1, vertices[face.2 as usize].0, vertices[face.2 as usize].1);
        }
        println!("</svg>");
    }
}